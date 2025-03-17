from django.urls import path
from .views import StudentListView, GroupListView, LessonListAPIView, LessonGroupListAPIView, AddLessonToGroupAPIView, TeacherListView, CreateLessonAPIView, TeacherGroupCreateView, TeacherGroupsView, AddTeacherToGroupView, CreateGroupView, CreateStudentView, CreateTeacherView, DeleteTeacherAPIView, DeleteStudentAPIView, DeleteGroupAPIView, DeleteLessonAPIView, AddStudentToGroupAPIView, GroupListAPIView, RemoveStudentFromGroupAPIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


app_name = "app_user"


urlpatterns = [
    path('create-teacher/', CreateTeacherView.as_view(), name='create-teacher'),
    path('create-student/', CreateStudentView.as_view(), name='create-student'),
    path('create-group/', CreateGroupView.as_view(), name='create-group'),
    path('add-teacher-to-group/', AddTeacherToGroupView.as_view(), name='add-teacher-to-group'),
    path('teacher-groups/<int:teacher_id>/', TeacherGroupsView.as_view(), name='teacher-groups'),
    path('teacher-group/create/', TeacherGroupCreateView.as_view(), name='teacher-group-create'),
    path('create-lesson/', CreateLessonAPIView.as_view(), name='create-lesson'),
    path('teacher/', TeacherListView.as_view(), name='teacher-list'),
    path('student/', StudentListView.as_view(), name='student-list'),
    path('group/', GroupListView.as_view(), name='group-list'),
    path('lessons/', LessonListAPIView.as_view(), name='lesson-list'),
    path('lesson-group/', LessonGroupListAPIView.as_view(), name='lesson-group-list'),
    path('add-lesson-group/', AddLessonToGroupAPIView.as_view(), name='add-lesson-group'),
    path('teacher-delete/', DeleteTeacherAPIView.as_view(), name='teacher-delete'),
    path('student-delete/', DeleteStudentAPIView.as_view(), name='student-delete'),
    path('group-delete/', DeleteGroupAPIView.as_view(), name='group-delete'),
    path('lesson-delete/', DeleteLessonAPIView.as_view(), name='lesson-delete'),
    path('add-student-to-group/', AddStudentToGroupAPIView.as_view(), name='add-student-to-group'),
    path('group/', GroupListAPIView.as_view(), name='group-list'),
    path('delete-group-student/', RemoveStudentFromGroupAPIView.as_view(), name='delete-group-student'),
]

urlpatterns += [
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]
