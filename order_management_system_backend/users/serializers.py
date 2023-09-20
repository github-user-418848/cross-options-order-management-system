from rest_framework import serializers
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        exclude = ['password']

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'name', 'age', 'password']

class UserChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_new_password = serializers.CharField(required=True)  # Add confirmation field

    def validate_current_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Incorrect current password")
        return value

    def validate(self, data):
        new_password = data.get('new_password')
        confirm_new_password = data.get('confirm_new_password')

        if new_password and confirm_new_password and new_password != confirm_new_password:
            raise serializers.ValidationError("New passwords do not match")

        return data