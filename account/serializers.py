from django.contrib.auth.models import User
from rest_framework import serializers

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]
    def validate_email(self, value):
        user = self.context['request'].user
        if User.objects.exclude(id=user.id).filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value