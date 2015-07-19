"""
Request:
--------
    {
       "username":"chennaisuperkings"
        "password":"password1234"
    }

Response:
---------
    {
        "result_msg": "List Of Tweets "
    }
    
"""
from django.contrib.auth.models import User
from miniter.models import Tweet
from miniter.models import Follower
from rest_framework import serializers
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


class Tweets_request_type(object):
    def __init__(self, username):
        self.username = username
class Tweets_request_serializer(serializers.Serializer):
    username = serializers.CharField()
    def create(self, validated_data):
        return Tweets_request_type(**validated_data)
    
class Tweets_response_type(object):
    def __init__(self, result_msg):
        self.result_msg = result_msg    

class Tweets_response_serializer(serializers.Serializer):
    
    result_msg = serializers.ListField()
    
    def create(self, validated_data):
        return Tweets_response_type(**validated_data)    

@api_view(['POST'])
def Tweets(request):
    
    request_serializer = Tweets_request_serializer(data = request.data)

    if request_serializer.is_valid():
        request_object = request_serializer.save()
        username = request_object.username
        result_msg=[];
        try :
                user=User.objects.get(username=username);
                comment=Tweet.objects.filter(user=user)
                for i in range(len(comment)):
                    result_msg.append(comment[i].message);
                Following=Follower.objects.filter(follower=user)
                for i in range(len(Following)):
                        person=Following[i].user
                        comment=Tweet.objects.filter(user=person)
                        for j in range(len(comment)):
                            result_msg.append(comment[j].message)
        except User.DoesNotExist:
                result_msg=["User Not Found"]
    else:
        result_msg = ["Json Details Sending Error"]
        
    result_msg_type = Tweets_response_type(result_msg = result_msg)
    
    response_serializer = Tweets_response_serializer(result_msg_type)
    
    return Response(data = response_serializer.data
                    ,status = status.HTTP_200_OK)
    
    
