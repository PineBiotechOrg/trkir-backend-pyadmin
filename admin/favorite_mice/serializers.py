from rest_framework import serializers

from .models import FavoriteMice


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteMice
        fields = '__all__'

