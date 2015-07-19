"""
Request:
--------
    {
        "username": "AK47",
        
    }

Response:
---------

    {
        "result_msg":"Followers list"
    }
    
"""

from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from miniter.models import Follower


class Followers_request_type(object):
    def __init__(self,username):
        self.username = username


class Followers_request_serializer(serializers.Serializer):
    
    username = serializers.CharField()

    
    def create(self, validated_data):
        return Followers_request_type(**validated_data)
    

class Followers_response_type(object):
    def __init__(self, result_msg):
        self.result_msg = result_msg    

class Followers_response_serializer(serializers.Serializer):
    
    result_msg = serializers.ListField()
    
    def create(self, validated_data):
        return Followers_response_type(**validated_data)    

@api_view(['POST'])
def get_followers(request):
    
    request_serializer = Followers_request_serializer(data = request.data)
    if request_serializer.is_valid():
        request_object = request_serializer.save()
        result_msg=[]
        try:
            user = User.objects.get(username=request_object.username)
            follower_objects=Follower.objects.filter(user=user)
            for element in follower_objects:
                result_msg.append(element.follower.username)  
        except User.DoesNotExist:
            result_msg=['User Doesnot Exist'] 
    else:
        result_msg = ["Invalid Json Data"]
    if len(result_msg)==0:
        result_msg=['No Followers For '+str(request_object.username)]
        
    result_msg_type = Followers_response_type(result_msg = result_msg)
    
    response_serializer = Followers_response_serializer(result_msg_type)
    
    return Response(data = response_serializer.data
                    ,status = status.HTTP_200_OK)