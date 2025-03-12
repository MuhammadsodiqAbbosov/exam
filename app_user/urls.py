from django.urls import path
from .views import CreateTeacherView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path

app_name = "app_user"


urlpatterns = [
    path('create-teacher/', CreateTeacherView.as_view(), name='create-teacher'),
]

urlpatterns += [
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
