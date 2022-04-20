from django.urls import path, include
from rest_framework.routers import DefaultRouter
from watchlist_app.api.views import (
    ReviewCreate, ReviewList,
    ReviewDetail, StreamPlatformViewSet,
    WatchlistViewSet, UserReview
    )


router = DefaultRouter() #Registering views in router allowing dynamic routing
router.register(r'watchlist', WatchlistViewSet,basename="watchlist")
router.register(r'stream', StreamPlatformViewSet, basename='stream') 

urlpatterns = [
    path('<int:pk>/review/',ReviewList.as_view(), name='review-list'),
    path('review/<int:pk>/',ReviewDetail.as_view(), name='review-detail'),
    path('reviews/',UserReview.as_view(), name='user-review-detail'),
    path('<int:pk>/review-create/',ReviewCreate.as_view(), name='review-create'),
    path('', include(router.urls)),
]