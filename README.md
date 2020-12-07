# BERT and Other Regressions of NLP

This folder contains all the source code for analyzing tweets with BERT and some other models.

## What to Do

You should run this on Google-Colab. It will provide all the libraries without hassel. Otherwise, you will need to install things like transformers, emoji, pandas, numpy, pytorch, tesnorflow.

### What to Run

#### TRAINING

You can make a brand new training session by running the cell to load the model in model\_save. You can then evaluate it. If you want to verify the data collected from the run in the report, running that cell also produces the dataloader needed since its a random split it wont be the same unless you load it in the cell... You must run a few other cells to get the optimizer and adam.

#### TESTING

You can test with the section of the notebook. It will produce graphs and such for you including how the training went.

#### Other Models

There are other models under that such as emoji linguistic analysis.

#### RECOMENDATIONS

We recommend you run as is and use the following steps:

Open a Colab instance uploading the notebook...
Upload the json files (this is temporary as the files will be removed after the notebook environment ends)
Upload the JSON from the celebrity folders, place the model\_save file as a zip into colab and unzip it with the command
`!unzip model_save.zip`. Then you can load in the zip....

If you do not want to upload the files (you must when using colab) you can run it locally and install any needed parts. Then you can substitute the directories in the code for ../data/CelebrityTweets for the celebirty tweets. Then you do not need to zip and unzip the model folder.


### JSON FORMATS

## Celebrities:
```
{"data": [
            {"text": "blah blah",
            "public_metrics": {
                "retweet_count": 4453",
                "reply_count": 454,
                "like_count": 434,
                "quote_count": 353
            }
        ],
  "user_info": {"public_metrics": {
                                    "followers_count": 3409,
                                    "following_count": 4535,
                                    "tweet_count: 535"},
                "name": "Ariana Grande",
                "username": "ArianaGrande"
                }
}
```
## Random Users:
```
{
    "data": [
        {
            "username": "3rachaed",
            "public_metrics": {
                "followers_count": 40,
                "following_count": 114,
                "tweet_count": 769,
                "listed_count": 3
            },
            "name": "dan⁷ is contemplating buying the hoodie",
            "id": "1318181368308895745",
            "tweetids": [
                "1329589572267814912",
                "1329584930490179587",
            ],
            "tweets": [
                {
                    "public_metrics": {
                        "retweet_count": 0,
                        "reply_count": 0,
                        "like_count": 0,
                        "quote_count": 0
                    },
                    "author_id": "1318181368308895745",
                    "text": "@carpediemskz 😌",
                    "id": "1329589572267814912",
                    "sentiment_score": 0.0001519918441772461
                },
                {
                    "public_metrics": {
                        "retweet_count": 0,
                        "reply_count": 1,
                        "like_count": 0,
                        "quote_count": 0
                    },
                    "author_id": "1318181368308895745",
                    "text": "aight aight gn!!!",
                    "id": "1329584930490179587",
                    "sentiment_score": 0.5
                }
            ]
        }
    ]
}
```

### Contributors

Joshua Bugryn (github:@bugryn-josh) and Josh Wilson also contributed to this project.
