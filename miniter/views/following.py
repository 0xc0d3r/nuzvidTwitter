'''

API for `Following` feature

request {
	"username" : "reboot"
}

response {
	"following_list" : [
		"anesh",
		"jana",
		"sunny",
		"aneesh"
	]
}
'''


from rest_framework import serializers
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User

from miniter.models import Follower

class Following_request_type(object):

	def __init__(self,username):
		self.username = username


class Following_request_serializer(serializers.Serializer):

	username = serializers.CharField()

	def create(self, validated_data):
		return Following_request_type(**validated_data)

class Following_response_type(object):

	def __init__(self,response_msg,following_list):
		self.response_msg = response_msg
		self.following_list = following_list

class Following_response_serializer(serializers.Serializer):

	response_msg = serializers.CharField()
	following_list = serializers.ListField(child = serializers.CharField())

	def create(self,validated_data):
		return Following_response_type(**validated_data)


def get_following_list(user):
	return [object.follower.username for object in Follower.objects.filter(user=user)]

@api_view(['POST'])
def following(request):

	request_serializer = Following_request_serializer(data = request.data)
	response_msg = ""
	following_list =[]
	if(request_serializer.is_valid()):

		request_object = request_serializer.save()
		user = None 

		try:
			user = User.objects.get(username = request_object.username)
			following_list = get_following_list(user)
			response_msg = "Followers List"
		except User.DoesNotExist:
			response_msg = "User not found"		
	else:
		response_msg = "Invalid JSON data"

	response_msg_type = Following_response_type(response_msg = response_msg,
												following_list = following_list)

	response_serializer = Following_response_serializer(response_msg_type)

	return Response(data = response_serializer.data,status = status.HTTP_200_OK)
