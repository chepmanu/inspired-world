from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import WrittingViewSet, TagListAPIView

app_name = "writtings"

router = DefaultRouter()
router.register('writtings', WrittingViewSet, base_name='writtings')

urlpatterns = [
    path('', include(router.urls)),
]
