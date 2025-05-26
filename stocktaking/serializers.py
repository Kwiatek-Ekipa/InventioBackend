from rest_framework import serializers

from stocktaking.models import Stocktaking


class StocktakingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stocktaking
        fields = "__all__"
        extra_kwargs = {
            'released_by' : { 'read_only': True },
            'release_date' : { 'read_only': True },
            'device' : { 'read_only': True }
        }

class TakeBackStocktakingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stocktaking
        fields = ['id']