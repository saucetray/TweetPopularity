from searchtweets import ResultStream, gen_request_parameters, load_credentials
import json
from searchtweets import collect_results
from requests_html import HTMLSession
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
import time
import sys
from bs4 import BeautifulSoup

bt = 'TWITTER API BEARER TOKEN MUST BE PLACED HERE IT HAS BEEN REMOVED FOR SECURITY REASONS'


def filt_forAuths(seq, value):
   for el in seq:
       if el.get('lang')!=value: yield el.get('author_id')

def filt_tweets(seq, value):
    for el in seq:
        if el.get('lang')==value: yield el

def filt_users(seq, values):
    for el in seq:
        print(el)
        if el.get('id') not in values: yield el


def remove_dups(tweets):
    de_dup = set()
    for t in tweets:
        if t.get('author_id') not in de_dup:
            de_dup.add(t.get('author_id'))
            yield t
        else:
            continue

def filter_for_en():

    obj = json.load(open('testJson.json', 'r', encoding='utf-8'))

    tweets = obj.get('data')
    users = obj.get('includes')

    author_ids = []
  
    author_ids = list(filt_forAuths(tweets, 'en'))

    tweet_filt = list(filt_tweets(tweets, 'en'))

    users_filt = list(filt_users(users, author_ids))
    

    obj['includes'] = users_filt

    json.dump(obj, open('enUsers.json', 'w'))



def getRecentTweets():
    endRecent = 'https://api.twitter.com/2/tweets/search/recent'

    search_args_rec = load_credentials(".twitter_keys.yaml",
                                    yaml_key="search_tweets_v2_recent",
                                    env_overwrite=False)


    query = {"max_results":100,"tweet.fields":"public_metrics,author_id,lang",
        "query":"happy -RT OR upset -RT OR lol -RT OR ugh -RT OR dog -RT OR cat -RT OR food -RT OR sucks -RT",
        "expansions": "author_id", "user.fields":"public_metrics"}
    

    rs = ResultStream(request_parameters=query,
                        endpoint=endRecent,
                        bearer_token=bt,
                        max_tweets=100,
                        max_requests=1,
                        )
    result = list(rs.stream())




    obj = {}

    obj['data'] = []
    obj['includes'] = []

    for r in result:
        obj['data'] = obj['data'] + r.get('data')
        obj['includes'] = obj['includes'] + r.get('includes').get('users')
    
    out = open('testJson.json', 'w')
    json.dump(obj, out)

def usersTweetsByIds():

    search_args1 = load_credentials(".twitter_keys.yaml",
                                    yaml_key="search_tweets_v2_id",
                                    env_overwrite=False)

    search_args2 = load_credentials(".twitter_keys.yaml",
                                    yaml_key="search_tweets_v2_user",
                                    env_overwrite=False)

    f = open('C:\\Users\\Josh\\Documents\\GitHub\\search-tweets-python\\enUsers_Tweets.json', 'r', encoding='utf-8')

    obj = json.load(f)

    for u in obj['includes']:

        idList = u.get('tweetids')

        ids = ''

        idList = list(set(idList))

        if len(idList) == 0:
            u['tweets'] = []
            continue

        if len(idList) > 99:
            ids = ','.join(idList[0:99])
        else:
            ids = ','.join(idList)


        endTweet = 'https://api.twitter.com/2/tweets'
    
    
        query = {"ids":ids,"tweet.fields":"author_id,public_metrics,text"}
        rs = ResultStream(request_parameters=query,
                            endpoint=endTweet,bearer_token=bt)


        tweets = []
        result = list(rs.stream())

        for r in result:

            tweets = r.get('data')

        u['tweets'] = tweets


    fo = open('Random_WithTweets.json', 'w', encoding='utf-8')
    json.dump(obj, fo)


def split_users():
    f = open('Random_WithTweets.json', 'r', encoding='utf-8')
    i = open('RandomUsers_WithTweets.json', 'r', encoding='utf-8')

    obj = json.load(f)

    output = json.load(i)    

    for u in obj.get('includes'):
        
        tweets = u.get('tweets')

        filt_tweets = []

        for t in tweets:
            if t.get('author_id') == u.get('id'):
                filt_tweets.append(t)
        
        u['tweets'] = filt_tweets


        if len(filt_tweets) > 0:
            output['data'].append(u)
    
    o = open('RandomUsers_WithTweets.json', 'w', encoding='utf-8')
    

    json.dump(output, o)


def genUserList():
    output = open('enUsers_Tweets.json', 'w', encoding='utf-8')

    input = open('enUsers.json','r',encoding='utf-8')

    input2 = open('idLists.json', 'r', encoding='utf-8')


    obj = json.load(input)

    obj2 = json.load(input2)

    for o, ts in zip(obj.get('includes'), obj2.get('tweets')):
        
        o['tweetids'] = []

        o['tweetids'] = ts


    json.dump(obj, output)


def genIdList():
    userList = open('userlist.txt', 'w')

    input = open('enUsers.json','r',encoding='utf-8')

    obj = json.load(input)

    users = []

    for u in obj.get('includes'):
        users.append(u['id'])
    
    for u in users:
        userList.write(u+'\n')



def getlatestTweetsUser():
    o = open('userlist.txt', 'r')


    tweetObj = {}

    tweetObj['tweets'] = []

    chrome_options = Options()
    chrome_options.add_argument('--headless')

    driver = webdriver.Chrome(
                executable_path=ChromeDriverManager().install(), options=chrome_options
        )
    driver.set_window_size(8000,7627)

    for line in o:
        url = "https://mobile.twitter.com/intent/user?user_id=" + line.strip()

        driver.get(url)

        time.sleep(15)
        results = driver.page_source
        soup = BeautifulSoup(results, "html.parser")

        tweets = soup.find_all('a')

        statuses = []


        for t in tweets:
            if t.get('href') != None:
                if 'status/' not in t.get('href') or 'photo' in t.get('href') or 'video' in t.get('href') or 'people' in t.get('href'):
                    continue
                else:
                    id = t.get('href').split('?')[0]
                    statuses.append(id)
        


        tweetids = []
        for s in statuses:
            d = s.split('status/')[1]
            tweetids.append(d)
        
        
        tweetObj['tweets'].append(tweetids)

    output = open('idLists.json', 'w+', encoding='utf-8')


    json.dump(tweetObj, output)



'''
    getreceentTweets -> filter_for_en -> genIdList -> genUserList -> getlatestTweets -> genUserList -> usersTweetsByIds -> split_users -> video_v2 get sentiments ::: result is randomusers_Withtweets_sentiment.json
'''

for i in range(0, 100):
    getRecentTweets()
    filter_for_en()
    genIdList()
    getlatestTweetsUser()
    genUserList()
    usersTweetsByIds()
    split_users()
    time.sleep(90)


