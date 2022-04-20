from rest_framework import serializers
from watchlist_app.models import Watchlist, StreamPlatform, Review


class ReviewSerializer(serializers.ModelSerializer):
    """Serializer for Review model"""
    review_user = serializers.StringRelatedField(
        read_only=True)  # replaces review_user true value, which is the id, with string related value (__str__)

    class Meta:
        model = Review
        exclude = ('watchlist',)  # excludes the watchlist field


class WatchlistSerializer(serializers.ModelSerializer):
    """Serializer for Watchlist model"""
    reviews = ReviewSerializer(
        many=True, read_only=True)  # Applying nested serializers (replacing the review field id with actual review model data fields)
    platform = serializers.CharField(source='platform.name')

    class Meta:
        model = Watchlist
        fields = '__all__'
        extra_kwargs = {
            'avg_rating': {'read_only': True},
            'number_rating': {'read_only': True}
        }


class StreamPlatformSerializer(serializers.ModelSerializer):
    """Stream platform serializer"""
    watchlist = WatchlistSerializer(many=True, read_only=True)

    class Meta:
        model = StreamPlatform
        fields = '__all__'
