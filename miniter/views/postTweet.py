"""
Request:
----------------------
	{ 
		"username":"Thanuja",
		"tweet":"Learning Django"
	}
Response:
--------------
	{
		"username":"Thanuja"
		"tweet" : "Learning Django"
		"result_msg": "Username not found"
	}
"""
from django.contrib.auth.models import User
from miniter.models import Tweet
from rest_framework import serializers
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

class Tweet_request_type(object):
    def __init__(self, username, tweet):
        self.username = username
        self.tweet = tweet
class Tweet_request_serializer(serializers.Serializer):
    username = serializers.CharField()
    tweet = serializers.CharField()
   
    def create(self, validated_data):
        return Tweet_request_type(**validated_data)

class Tweet_response_type(object):
    def __init__(self, username, tweet,result_msg):
        self.username = username
        self.tweet = tweet
        self.result_msg = result_msg  

class Tweet_response_serializer(serializers.Serializer):
    username = serializers.CharField()
    tweet = serializers.CharField()
    result_msg = serializers.CharField()
    def create(self, validated_data):
        return Tweet_response_type(**validated_data)
def create_new_tweet(user, tweet):
    
    try:
        user = Tweet.objects.create(user=user,message=tweet)
    except:
        user = None
    
    return user
@api_view(['POST'])
def postTweet(request):
	tweet_serializer = Tweet_request_serializer(data = request.data)
        if tweet_serializer.is_valid():
            tweet_object = tweet_serializer.save()
            username = tweet_object.username
            tweet = tweet_object.tweet
            if len(tweet) > 140:
                result_msg = "Tweet lenght lime is over"
            else:            
                user = None
                try:
                    user = User.objects.get(username=username)
                    user = user = create_new_tweet(user, tweet)
                    if user is not None:
                        result_msg = "Done"
                except User.DoesNotExist:
                    result_msg = "Username not found" 
    	else:
    		result_msg = "Invalid Json Data"
    			
    	result_msg_type = Tweet_response_type(username=username, tweet=tweet, result_msg=result_msg)
        
        response_serializer = Tweet_response_serializer(result_msg_type)
        
        return Response(data = response_serializer.data, status = status.HTTP_200_OK)
