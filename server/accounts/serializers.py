from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8 ,style={'input_type': 'password'}) #write_only means pass should only write through post put or patch it should not retrieve
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        #  User.objects.create() = save the password in plain text
        # User.objects.create_user() = automatically hash the password
        # user = User.objects.create_user(**validated_data) = used this when you need all fields during creation of user 
        user = User.objects.create_user(
             validated_data['username'],
             validated_data['email'],
             validated_data['password'],
            )
         
        return user