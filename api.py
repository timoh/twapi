apikeys = __import__('apikeys')
from twitter import *
t = Twitter(auth=OAuth(apikeys.access_token_key, apikeys.access_token_secret,apikeys.consumer_key, apikeys.consumer_secret))

api_limit_reset_in_seconds = 900 # 15 minutes in seconds


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

all_users = friends_coll.find().count()
print("Amount of friends, total: ",str(all_users))

tweet_count = tweets_coll.find().count()
print("Amount of tweets stored, total:" ,str(tweet_count))

# 1. find people with tweets and take those as a list
peeps_set = set()
pwt = tweets_coll.find()
for i in pwt:
    peeps_set.add(i['twitter_user_id'])

peeps_with_tweets = []
peeps_with_tweets = list(peeps_set)

a = friends_coll.find({ 'twitter_user_id': { '$nin': peeps_with_tweets } }) # this doesn't work as expected, still returns all users..


def printingSleeper(secs):
    total_time = secs
    from time import sleep
    import datetime
    time_now = datetime.datetime.now().time().strftime('%H:%S')
    diff = datetime.timedelta(milliseconds=total_time)
    projected_end_time = ((datetime.datetime.now()+diff).time().strftime('%H:%S'))
    print("Starting to sleep a total of ", str(total_time/60), "minutes. Time now: ",str(time_now), ". Time at the end: ",str(projected_end_time))
    fractions = 60
    fractional_time = int(total_time/fractions)
    counter = 0
    while counter < fractions:
        time_remaining = total_time - ( fractional_time * (counter) )
        print("Now sleeping for ", str(fractional_time), " seconds.")
        print("Total sleep remaining: ", str(time_remaining/60), " minutes.")
        counter = counter+1
        sleep(fractional_time)

def getTweetsForUsers(users_array):
    total_num = users_array.count()
    print("Starting to fetch tweets for ", str(total_num), " users.. \n\n")
    counter = 0
    for user in users_array:
        counter = counter+1
        print("Operation ", str(counter), " of ", str(total_num), " operations total.")
        twuid = str(user['twitter_user_id'])
        if twuid not in peeps_with_tweets:
            print("Fetching tweets for user ",str(twuid))
            try:
                st = t.statuses.user_timeline(user_id=twuid)
                if len(st) > 0:
                    tweets_coll.insert_many([{'twitter_user_id': twuid, 'raw_tweet': tweet} for tweet in st ])
                    print("Done storing all tweets for user. \n")
                else:
                    print("No tweets to store for this user.")
            except KeyboardInterrupt:
                print("Interrupted by user. Exiting.")
                pass
                break
            except Exception as err:
                from time import sleep
                print("\n\n\n Problem! \n\n\n Waiting 15 minutes due to probable API limit reached.")
                print("Error: ", err)
                printingSleeper(api_limit_reset_in_millis)
            except:
                import sys
                print("Error:", sys.exc_info()[0])
    if total_num <= counter:
        print("Fetching all tweets for all uses completed successfully!")
    else:
        print("Fetching aborted.")
# done

getTweetsForUsers(a)











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
