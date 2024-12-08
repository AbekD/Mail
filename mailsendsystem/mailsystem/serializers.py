import io

from rest_framework import serializers
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

from .models import User

# class UserModel:
#     def __init__(self, first_name, message):
#         self.first_name = first_name
#         self.message = message


class SendMessageSerializer(serializers.Serializer):
    users = serializers.ListField(
        child=serializers.IntegerField(),
        required=True
    )
    message = serializers.CharField(required=True)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


    # id = serializers.IntegerField(read_only=True)
    # email = serializers.EmailField()
    # first_name = serializers.CharField(max_length=255)
    # last_name = serializers.CharField(max_length=255)
    # message = serializers.CharField()
    # time_created = serializers.DateTimeField(read_only=True)
    # time_updated = serializers.DateTimeField(read_only=True)
    # is_published = serializers.BooleanField(default=True)
    #
    #
    # def create(self, validated_data):
    #     return User.objects.create(**validated_data)
    #
    # def update(self, instance, validated_data):
    #     instance.email = validated_data.get("email", instance.email)
    #     instance.first_name = validated_data.get("first_name", instance.first_name)
    #     instance.last_name = validated_data.get("last_name", instance.last_name)
    #     instance.message = validated_data.get("message", instance.message)
    #     instance.time_created = validated_data.get("time_created", instance.time_created)
    #     instance.time_updated = validated_data.get("time_updated", instance.time_updated)
    #     instance.is_published = validated_data.get("is_published", instance.is_published)
    #     instance.save()
    #     return instance



# def encode():
#     model = UserModel('John','Message:you got some message')
#     model_sr = UserSerializer(model)
#     print(model_sr.data, type(model_sr.data), sep='\n')
#     json = JSONRenderer().render(model_sr.data)
#     print(json)
#
#
# def decode():
#     stream = io.BytesIO(b'{"first_name":"John","message":"Message:you got some message"}')
#     data = JSONParser().parse(stream)
#     serializer = UserSerializer(data=data)
#     serializer.is_valid()
#     print(serializer.validated_data)