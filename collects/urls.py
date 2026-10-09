from rest_framework.routers import DefaultRouter

from .views import CollectViewSet

router = DefaultRouter()
router.register('collects', CollectViewSet, basename='collect')

urlpatterns = router.urls