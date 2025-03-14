from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Teacher
from .serializers import TeacherSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from .models import CustomUser
from .serializers import TeacherSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Teacher, Student
from .serializers import TeacherSerializer, StudentSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import CustomUser
from .serializers import TeacherSerializer
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Teacher
from .serializers import TeacherSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from .models import CustomUser
from .serializers import TeacherSerializer
from .serializers import GroupSerializer
from .models import Group
from rest_framework import status
from rest_framework.response import Response
from app_user.models import TeacherGroup
from .serializers import TeacherGroupSerializer


class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff

class CreateTeacherView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = TeacherSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

    def create(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied("Sizda ushbu amalni bajarish uchun ruxsat yo'q.")
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({"message": "O'qituvchi muvaffaqiyatli yaratildi", "user": TeacherSerializer(user).data})


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})
    
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        
        data.update({
            "user_id": self.user.id,
            "username": self.user.username,
            "email": self.user.email,
        })
        
        return data

@method_decorator(csrf_exempt, name='dispatch')
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            return Response({"error": "Login yoki parol noto‘g‘ri!"}, status=status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.validated_data, status=status.HTTP_200_OK)
    


class CreateTeacherView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        serializer = TeacherSerializer(data=request.data)
        if serializer.is_valid():
            teacher = serializer.save()
            return Response({"message": "Teacher created successfully!", "data": TeacherSerializer(teacher).data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        teachers = Teacher.objects.all()
        if not teachers.exists():
            return Response({"message": "No teachers found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = TeacherSerializer(teachers, many=True)
        return Response(serializer.data)


class CreateStudentView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            student = serializer.save()
            return Response({"message": "Student created successfully!", "data": StudentSerializer(student).data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        students = Student.objects.all()
        if not students.exists():
            return Response({"message": "No students found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)
    

class CreateGroupView(generics.CreateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class AddTeacherToGroupView(APIView):
    def post(self, request):
        teacher_id = request.data.get('teacher_id')
        group_ids = request.data.get('group_ids', [])

        try:
            teacher = Teacher.objects.get(id=teacher_id)
            groups = Group.objects.filter(id__in=group_ids)

            teacher.groups.add(*groups)  # Teacher ga bir nechta group qo‘shish
            teacher.save()

            return Response(
                {"message": "Teacher successfully added to groups"},
                status=status.HTTP_200_OK
            )
        except Teacher.DoesNotExist:
            return Response(
                {"error": "Teacher not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        

class TeacherGroupsView(APIView):
    def get(self, request, teacher_id):
        try:
            teacher = Teacher.objects.get(id=teacher_id)
            groups = teacher.groups.all()
            group_data = [{"id": g.id, "name": g.name} for g in groups]

            return Response({"groups": group_data}, status=status.HTTP_200_OK)
        except Teacher.DoesNotExist:
            return Response(
                {"error": "Teacher not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        
class TeacherGroupCreateView(generics.CreateAPIView):
    queryset = TeacherGroup.objects.all()
    serializer_class = TeacherGroupSerializer

class TeacherGroupListView(generics.ListAPIView):
    queryset = TeacherGroup.objects.all()
    serializer_class = TeacherGroupSerializer