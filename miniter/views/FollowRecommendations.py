"""
Request:
--------
    {
	famous personalities list : usernames list
     }

 Example I/P :: {famous_usernames":"["namo","sachin","deepika","virat","anushka"]"}

Response:
---------

    {
       list of recommended followers : usernames list 
    }

	
 Example O/P :: {famous_usernames":"["namo","sachin","deepika","virat","anushka"]"}
    
"""
from miniter.models import Follower
from rest_framework import serializers
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


class FollowRecommendations_request_type(object):
    def __init__(self, famous_usernames):
       
        self.famous_usernames = famous_usernames
	#self.previous_usernames = previous_usernames

class FollowRecommendations_request_serializer(serializers.Serializer):
    
   famous_usernames = serializers.ListField()
   #previous_usernames = serializers.ListField()
   def create(self, validated_data):
        return FollowRecommendations_request_type(**validated_data)

class FollowRecommendations_response_type(object):
    def __init__(self,  RecommendedFollowers  ):
        self.RecommendedFollowers = RecommendedFollowers   

class FollowRecommendations_response_serializer(serializers.Serializer):
    
    RecommendedFollowers = serializers.ListField()
    
    def create(self, validated_data):
        return FollowRecommendations_response_type(**validated_data)  

@api_view(['POST'])
def FollowRecommendations(request):
    
    request_serializer = FollowRecommendations_request_serializer(data = request.data)

    if request_serializer.is_valid():
        request_object = request_serializer.save()
        
	result_msg= request_object.famous_usernames
	#previous_users = request_object.previous_usernames
    else:
        result_msg = ["No records found"]
        
    result_msg_type =  FollowRecommendations_response_type(RecommendedFollowers = result_msg)
    
    response_serializer = FollowRecommendations_response_serializer(result_msg_type)
    
    return Response(data = response_serializer.data,status = status.HTTP_200_OK)
    

