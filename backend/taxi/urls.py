from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register('travel', views.ArtWorkViewSet, basename='travel')
router.register('history', views.ArtWorkViewSet, basename='history')


urlpatterns = router.urls
