from rest_framework_nested import routers
from django.urls import path
from . import views

router = routers.DefaultRouter()
router.register('travel', views.TravelViewSet, basename='travel')
router.register('history', views.HistoryViewSet, basename='history')

api_url = [
    path('find_place/', views.FindPlace.as_view()),
    path('find_distance/', views.FindDistance.as_view()),
    path('travel_to_history/', views.TravelToHistory.as_view()),
    path('fixed_places/', views.TravelFixedPlacesApi.as_view()),
]

urlpatterns = router.urls + api_url
