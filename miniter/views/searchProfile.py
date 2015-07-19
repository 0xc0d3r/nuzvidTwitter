from django.contrib.auth.models import User

from rest_framework import serializers
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response



class Search_request_type(object):
    def __init__(self,username):
        self.username=username
        
        
class Search_request_serializer(serializers.Serializer):
    username = serializers.CharField()
    
    def create(self, validated_data):
        return Search_request_type(**validated_data)

class SearchProfile_response_type(object):
    def __init__(self,result_search_msg):
        self.result_search_msg= result_search_msg
class Search_response_serializer(serializers.Serializer):
    result_search_msg = serializers.CharField()
    def create(self, validated_data):
        return SearchProfile_response_type(**validated_data)    

@api_view(['POST'])
def search(request):
    request_serializer = Search_request_serializer(data = request.data)
    
    if request_serializer.is_valid():
        request_object = request_serializer.save()
        
    user_name = request_object.username;
    result_search_msg = "User "+user_name+" Found"
    user = None
    try:
        user = User.objects.get(username=user_name)
    except User.DoesNotExist:
        result_search_msg = "User "+user_name+" Not Found"
    

    result_msg_type = SearchProfile_response_type(result_search_msg = result_search_msg)
    response_serializer = Search_response_serializer(result_msg_type)

    return Response(data=response_serializer.data,status = status.HTTP_200_OK)