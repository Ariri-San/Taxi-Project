from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register('travel', views.TravelViewSet, basename='travel')
router.register('history', views.HistoryViewSet, basename='history')


urlpatterns = router.urls
