from rest_framework.routers import DefaultRouter
from .views import UsersView

router = DefaultRouter()

router.register(r'users', UserView, basename='users')
urlpatterns = router.urls