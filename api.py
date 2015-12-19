apikeys = __import__('apikeys')
from twitter import *
t = Twitter(auth=OAuth(apikeys.access_token_key, apikeys.access_token_secret,apikeys.consumer_key, apikeys.consumer_secret))
t.statuses.home_timeline()
print(t)

# t.application.rate_limit_status()
friends = t.friends.ids()
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

#friends_coll.insert_many([{'twitter_user_id': f_id} for f_id in friends['ids'] ])

a = friends_coll.find_one()




# import datetime
# post = {"author": "Mike",
#         "text": "My first blog post!",
#         "tags": ["mongodb", "python", "pymongo"],
#         "date": datetime.datetime.utcnow()}

rlimits = api.GetRateLimitStatus()

# print rlimits[u'resources'][u'friends'][u'/friends/list'].keys()

flimits = rlimits[u'resources'][u'friends'][u'/friends/list']
idlimits = rlimits[u'resources'][u'friends'][u'/friends/ids']



print(rlimits[u'resources'][u'friends'])

# {u'reset': 1448543020, u'limit': 15, u'remaining': 0}

import datetime
print(
    datetime.datetime.fromtimestamp(
        flimits[u'reset']
    ).strftime('%Y-%m-%d %H:%M:%S')
)

print(flimits)

print("Attempting to get friend IDs from API")
print(idlimits)
friends_res = api.GetFriendIDs()

print(friends_res)

# for i in friends_res:
#     friend = friends_coll.insert_one(i)

#for i in friends:
