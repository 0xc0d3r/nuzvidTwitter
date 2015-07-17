'''

API for `Following` feature

request {
	"user_id" : "reboot"
}

response {
	"followingList" : "["anesh","jana","sunny","aneesh"]"
}
'''

db_users_list = ["anesh","jana","reboot","sunny"]

from rest_framework import serializers
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

class Following_request_type(object):

	def __init__(self,user_id):
		self.user_id = user_id


class Following_request_serializer(serializers.Serializer):

	user_id = serializers.CharField()

	def create(self, validated_data):
		return Following_request_type(**validated_data)

class Following_response_type(object):

	def __init__(self,response_msg):
		self.response_msg = response_msg

class Following_response_serializer(serializers.Serializer):

	response_msg = serializers.CharField()

	def create(self,validated_data):
		return Following_response_type(**validated_data)



@api_view(['POST'])
def following(request):

	request_serializer = Following_request_serializer(data = request.data)
	response_msg = ""
	if(request_serializer.is_valid()):

		request_object = request_serializer.save()

		user_id = request_object.user_id

		if user_id not in db_users_list:
			response_msg = "User not found"
		else:
			response_msg = "Followers List"
	else:
		response_msg = "Invalid JSON data"

	response_msg_type = Following_response_type(response_msg = response_msg)

	response_serializer = Following_response_serializer(response_msg_type)

	return Response(data = response_serializer.data,status = status.HTTP_200_OK)
