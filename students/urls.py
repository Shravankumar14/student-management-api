from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    StudentViewSet,
    CourseViewSet,
    profile,
    register_user,
    logout_user,
)

router = DefaultRouter()

router.register(
    r'students',
    StudentViewSet
)

router.register(
    r'courses',
    CourseViewSet
)


from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [

    path(
        'register/',
        register_user,
        name='register_user'
    ),

    path(
    'api/token/refresh/',
    TokenRefreshView.as_view(),
    name='token_refresh'
),
    path(
        'logout/',
        logout_user,
        name='logout_user'
    ),

    path('profile/', profile, name='profile'),

]

urlpatterns += router.urls