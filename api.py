apikeys = __import__('apikeys')
from twitter import *
t = Twitter(auth=OAuth(apikeys.access_token_key, apikeys.access_token_secret,apikeys.consumer_key, apikeys.consumer_secret))

api_limit_reset_in_millis = 900100 # 15 minutes in millis


#t.statuses.home_timeline()
#print(t)

# t.application.rate_limit_status()
# friends = t.friends.ids()
# api = twitter.Api(consumer_key=apikeys.consumer_key, consumer_secret=apikeys.consumer_secret,access_token_key=apikeys.access_token_key, access_token_secret=apikeys.access_token_secret)
# if ( not api.VerifyCredentials() ):
#     print("Fail!")
# else:
#     print("Yep")

import pymongo
from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.twapi
friends_coll = db.friends
tweets_coll = db.tweets

#friends_coll.insert_many([{'twitter_user_id': f_id} for f_id in friends['ids'] ])

# need to find those people with no tweets stored

# 1. find people with tweets and take those as a list
peeps_with_tweets = []
pwt = tweets_coll.find().distinct("twitter_user_id")
for i in pwt:
    peeps_with_tweets.append(i)

a = friends_coll.find({ 'twitter_user_id': { '$nin': peeps_with_tweets } })

def getTweetsForUsers(users_array):
    total_num = users_array.count()
    print("Starting to fetch tweets for ", str(total_num), " users.. \n\n")
    counter = 0
    for user in users_array:
        counter = counter+1
        print("Operation ", str(counter), " of ", str(total_num), " operations total.")
        twuid = str(user['twitter_user_id'])
        print("Fetching tweets for user ",str(twuid))
        try:
            st = t.statuses.user_timeline(user_id=twuid)
            tweets_coll.insert_many([{'twitter_user_id': twuid, 'raw_tweet': tweet} for tweet in st ])
            print("Done storing all tweets for user. \n")
        except:
            from time import sleep
            print("\n\n\n Problem! \n\n\n Waiting 15 minutes due to probable API limit reached.")
            sleep(api_limit_reset_in_millis)
# done

getTweetsForUsers(a)

print("Fetching all tweets for all uses completed successfully!")









# import datetime
# post = {"author": "Mike",
#         "text": "My first blog post!",
#         "tags": ["mongodb", "python", "pymongo"],
#         "date": datetime.datetime.utcnow()}

#rlimits = api.GetRateLimitStatus()

# print rlimits[u'resources'][u'friends'][u'/friends/list'].keys()

#flimits = rlimits[u'resources'][u'friends'][u'/friends/list']
#idlimits = rlimits[u'resources'][u'friends'][u'/friends/ids']



#print(rlimits[u'resources'][u'friends'])

# {u'reset': 1448543020, u'limit': 15, u'remaining': 0}

#import datetime
# print(
#     datetime.datetime.fromtimestamp(
#         flimits[u'reset']
#     ).strftime('%Y-%m-%d %H:%M:%S')
# )

# print(flimits)
#
# print("Attempting to get friend IDs from API")
# print(idlimits)
# friends_res = api.GetFriendIDs()
#
# print(friends_res)

# for i in friends_res:
#     friend = friends_coll.insert_one(i)

#for i in friends:
