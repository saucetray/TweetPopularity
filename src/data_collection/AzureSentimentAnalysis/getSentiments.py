import pandas as pd
import json
import requests
import ast
import yaml
import glob
import pathlib
cwd =  pathlib.Path(__file__).parent.absolute()


def create_twitter_url():
    handle = "ArianaGrande"
    max_results = 100
    mrf = "max_results={}".format(max_results)
    q = "query=from:{}".format(handle)
    url = "https://api.twitter.com/2/tweets/search/recent?tweet.fields=lang&{}&{}".format(
        mrf, q
    )
    return url


def process_yaml():
    with open("config.yaml") as file:
        return yaml.safe_load(file)


def create_bearer_token(data):
    return data["search_tweets_api"]["bearer_token"]


def connect_to_azure(data):
      azure_url = "https://week.cognitiveservices.azure.com/"
      sentiment_url = "{}text/analytics/v2.1/sentiment".format(azure_url)
      subscription_key = data["azure"]["subscription_key"]
      return sentiment_url, subscription_key


def azure_header(subscription_key):
    return {"Ocp-Apim-Subscription-Key": subscription_key}


# Connect to Twitter
def twitter_auth_and_connect(bearer_token, url):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    response = requests.request("GET", url, headers=headers)
    return response.json()


def create_document_format(res_json):
    #data_only = res_json["data"]
    doc_start = '"documents": {}'.format(res_json)
    str_json = "{" + doc_start + "}"
    dump_doc = json.dumps(str_json)
    doc = json.loads(dump_doc)
    return ast.literal_eval(doc)


# Get sentiment scores
def sentiment_scores(headers, sentiment_url, document_format):
    response = requests.post(sentiment_url, headers=headers, json=document_format)
    return response.json()


def mean_score(sentiments):
    sentiment_df = pd.DataFrame(sentiments["documents"])
    return sentiment_df["score"].mean()


def main2():
    data = process_yaml()

    jsons = glob.iglob('celebjsons/*.json')

    for j in jsons:
        name = j.split('\\')[1].split('.')[0]
        outputfile = j.split('\\')[1]
        fi = open(j, 'r', encoding='utf-8')

        res_json = json.load(fi)

        output_json = res_json

        output_json['user_info'] = {}

        for i in output_json.get('includes').get('users'):
            if str(i.get('username')).lower() == name.lower():
                output_json['user_info'] = i
        
        output_json.pop('includes')


        tweets = output_json.get('data')

        t_ids = set()

        tweets_filt = []

        for t in tweets:
            if t.get('id') not in t_ids:
                t_ids.add(t.get('id'))
                tweets_filt.append(t)
            else:
                continue
        
        output_json['data'] = tweets_filt


        document_format = create_document_format(tweets_filt)

    
        sentiment_url, subscription_key = connect_to_azure(data)
        headers = azure_header(subscription_key)
        sentiments = sentiment_scores(headers, sentiment_url, document_format)

        for s,t in zip(sentiments["documents"], output_json['data']):
            t["sentiment_score"] = s["score"]
    
        fi = open('sentcelebs\\' + outputfile, 'w', encoding='utf-8')

        json.dump(output_json, fi)

def main():
    data = process_yaml()

    fi = open('RandomUsers_WithTweets.json','r',encoding='utf-8')

    res_json = json.load(fi)

    output_json = res_json

    for u in output_json.get('data'):

        tweets = u.get('tweets')

        t_ids = set()

        tweets_filt = []

        for t in tweets:
            if t.get('id') not in t_ids:
                t_ids.add(t.get('id'))
                tweets_filt.append(t)
            else:
                continue
        
        u['tweets'] = tweets_filt


        document_format = create_document_format(tweets_filt)

    
        sentiment_url, subscription_key = connect_to_azure(data)
        headers = azure_header(subscription_key)
        sentiments = sentiment_scores(headers, sentiment_url, document_format)

        for s,t in zip(sentiments["documents"], u['tweets']):
            t["sentiment_score"] = s["score"]
    
    fi = open('output\\RandomUsers_WithTweets_Sentiments.json', 'w', encoding='utf-8')

    json.dump(output_json, fi)

if __name__ == "__main__":
    #// for random user data
    main()

    # for celeb user data
    #main2()
