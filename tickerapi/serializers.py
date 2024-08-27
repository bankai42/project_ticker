from rest_framework import serializers
from django.contrib.auth.models import User
from tickerapp.models import Ticker

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_staff']

class TickerSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)

    class Meta:
        model = Ticker
        fields = ['id', 'owner', 'text', 'timestamp', 'video_file', 'filename']