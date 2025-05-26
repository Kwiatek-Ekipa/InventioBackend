from rest_framework import serializers

from stocktaking.models import Stocktaking


class StocktakingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stocktaking
        fields = "__all__"

class TakeBackStocktakingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stocktaking
        fields = ['id']