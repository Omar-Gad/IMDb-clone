from rest_framework import viewsets, generics, filters
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle, ScopedRateThrottle

from django_filters.rest_framework import DjangoFilterBackend

from watchlist_app.models import Watchlist, StreamPlatform, Review
from watchlist_app.api.serializers import WatchlistSerializer, StreamPlatformSerializer, ReviewSerializer
from watchlist_app.api.permissions import IsAdminOrReadOnly, IsReviewOwnerOrReadOnly
from watchlist_app.api.throttoling import ReviewDetailThrottle


class UserReview(generics.ListAPIView):
    """Listing Reviews according to review owner"""
    serializer_class = ReviewSerializer
    throttle_classes = [ReviewDetailThrottle,]

    def get_queryset(self):
        username = self.request.query_params.get('username', None)
        return Review.objects.filter(review_user__username=username)


class ReviewCreate(generics.CreateAPIView):
    """Create new reviews"""
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated,]
    
    def get_queryset(self):
        return Review.objects.all()

    def perform_create(self, serializer): #Create review only for the provided watchlist pk in the url
        
        pk = self.kwargs.get('pk')
        watchlist = Watchlist.objects.get(pk=pk)
        review_user = self.request.user
        review_queryset = Review.objects.filter(
            watchlist=watchlist,
            review_user=review_user
            )

        if review_queryset.exists():
            raise ValidationError('You have already reviewed this watchlist!')

        if watchlist.number_rating == 0:
            watchlist.avg_rating = serializer.validated_data['rating']
        else:
            watchlist.avg_rating = (
                watchlist.avg_rating + serializer.validated_data['rating']
                ) / 2
        
        watchlist.number_rating += 1
        watchlist.save()

        serializer.save(watchlist=watchlist, review_user=review_user)


class ReviewList(generics.ListAPIView):
    """Listing Reviews according to their movies"""
    serializer_class = ReviewSerializer
    throttle_classes = [ReviewDetailThrottle,]
    filter_backends = [DjangoFilterBackend,]
    filterset_fields = ['review_user', 'rating']

    def get_queryset(self): #List reviews only for the provided watchlist pk in the url
        pk = self.kwargs['pk']
        return Review.objects.filter(watchlist=pk)


class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    """Updating and deleting user's review"""
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()
    permission_classes = [IsReviewOwnerOrReadOnly,]
    throttle_classes = [AnonRateThrottle, UserRateThrottle,]


class StreamPlatformViewSet(viewsets.ModelViewSet):
    """Model viewset for Streaming platforms"""
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer
    permission_classes = [IsAdminOrReadOnly,]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    


class WatchlistViewSet(viewsets.ModelViewSet):
    """Model viewset for Watchlists"""
    queryset = Watchlist.objects.all()
    serializer_class = WatchlistSerializer
    permission_classes = [IsAdminOrReadOnly,]
    throttle_classes = [ScopedRateThrottle,]
    throttle_scope = 'watchlist'
    filter_backends = [DjangoFilterBackend,filters.SearchFilter]
    filterset_fields = ['reviews__rating']
    search_fields = ['title']
