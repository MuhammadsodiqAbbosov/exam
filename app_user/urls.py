from django.urls import path
from app_user.views import CreateTeacherView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path
from app_user.views import CreateTeacherView, CreateStudentView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path
from app_user.views import CreateTeacherView, CreateStudentView, CreateGroupView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path
from app_user.views import CreateTeacherView, CreateStudentView, CreateGroupView, AddTeacherToGroupView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path
from app_user.views import CreateTeacherView, CreateStudentView, CreateGroupView, AddTeacherToGroupView, TeacherGroupsView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path
from app_user.views import CreateTeacherView, CreateStudentView, CreateGroupView, AddTeacherToGroupView, TeacherGroupsView, TeacherGroupListView, TeacherGroupCreateView
app_name = "app_user"


urlpatterns = [
    path('create-teacher/', CreateTeacherView.as_view(), name='create-teacher'),
    path('create-student/', CreateStudentView.as_view(), name='create-student'),
    path('create-group/', CreateGroupView.as_view(), name='create-group'),
    path('add-teacher-to-group/', AddTeacherToGroupView.as_view(), name='add-teacher-to-group'),
    path('teacher-groups/<int:teacher_id>/', TeacherGroupsView.as_view(), name='teacher-groups'),
    path('teacher-group/', TeacherGroupListView.as_view(), name='teacher-group-list'),
    path('teacher-group/create/', TeacherGroupCreateView.as_view(), name='teacher-group-create'),
]

urlpatterns += [
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]
