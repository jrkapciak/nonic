from django.contrib.auth import get_user_model
from rest_framework import serializers

UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    class Meta:
        model = UserModel
        fields = ("id", "username", "password", "email", "phone")

    def create(self, validated_data) -> UserModel:
        password = validated_data.pop("password", None)
        instance = self.Meta.model(**validated_data)

        if password and not instance.password:
            instance.set_password(password)
        instance.save()
        return instance
