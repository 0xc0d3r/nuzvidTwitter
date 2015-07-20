"""
Request:
--------
    {
        "user_id":"U123",
       	"follower_id":"F321"
    }

Response:
---------

    {
        "result_msg": "Success" or "Failed"
    }
    
"""
from django.contrib.auth.models import User
from miniter.models import Follower

from rest_framework import serializers
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

class Follow_unfollow_request_type(object):
	def __init__(self, user_id,follower_id):
		self.user_id=user_id
		self.follower_id=follower_id

class Follow_unfollow_request_serializer(serializers.Serializer):
    
	user_id = serializers.CharField()
	follower_id = serializers.CharField()
    
	def create(self, validated_data):
		return Follow_unfollow_request_type(**validated_data)
        
       
class Follow_unfollow_response_type(object):
	def __init__(self,result_msg):
		self.result_msg=result_msg
        
class Follow_unfollow_response_serializer(serializers.Serializer):
    
	result_msg = serializers.CharField()
	
	def create(self, validated_data):
		return Follow_unfollow_response_type(**validated_data)            
		
def add_follower(user_id,follower_id):
    
	try:
		follow = Follower.objects.create(user = user_id,follower=follower_id)
	except:
		follow = None

	return follow
    		
@api_view(['POST'])
def followUnfollow(request):
	request_serializer = Follow_unfollow_request_serializer(data=request.data)
	result_msg="Failed"
	if request_serializer.is_valid():
		request_object = request_serializer.save()
		user_id=request_object.user_id
		follower_id=request_object.follower_id
		
		user = None
		follower=None
		follow=None
		follow_status=None
		try:
			user = User.objects.get(username=user_id)
		except User.DoesNotExist:
			result_msg="User is not exist!!!"
		try:
			follower = User.objects.get(username=follower_id)
		except User.DoesNotExist:
			result_msg="Follower is not exist!!!"
		print "user",user,follower
		if(user is not None) and (follower is not None):
			try:
				follow=Follower.objects.get(user=user,follower=follower).delete()
				print "fol",follow
				result_msg="Successfully unfollowed "
			except Follower.DoesNotExist:
				follow=add_follower(user,follower)
				result_msg="Successfully followed "
				
		elif(user is None) and (follower is None):
			result_msg="Both user and follower are not exist"

		
	else:
		result_msg="Invalid JSON object"
		print "koti"
		
	result_msg_type = Follow_unfollow_response_type(result_msg = result_msg)
	response_serializer = Follow_unfollow_response_serializer(result_msg_type)
	return Response(data = response_serializer.data,status = status.HTTP_200_OK)
