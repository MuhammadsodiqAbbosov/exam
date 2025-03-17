from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, generics, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import PermissionDenied
from .serializers import TeacherSerializer, CustomTokenObtainPairSerializer, TeacherSerializer, StudentSerializer, GroupSerializer, TeacherGroupSerializer, LessonSerializer
from app_user.models import CustomUser, Student, Group, Teacher, TeacherGroup, Lesson 
import json
from rest_framework.generics import ListAPIView




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
            return Response({"error": "Login yoki parol notogri!"}, status=status.HTTP_401_UNAUTHORIZED)

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

            teacher.groups.add(*groups)
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

class CreateLessonView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        teacher = self.request.user
        groups = serializer.validated_data.get('groups', [])

        allowed_groups = teacher.groups.all()

        if not set(groups).issubset(set(allowed_groups)):
            return Response({"error": "Siz faqat oz guruhlaringiz uchun dars yaratishingiz mumkin."}, status=403)

        serializer.save(teacher=teacher)

class CreateLessonAPIView(APIView):
    def post(self, request):
        title = request.data.get("title")
        content = request.data.get("content")
        group_ids = request.data.get("groups", [])
        teacher_id = request.data.get("teacher")

        if not title or not content or not teacher_id:
            return Response({"error": "title, content va teacher kerak!"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            teacher = Teacher.objects.get(id=teacher_id)
            lesson = Lesson.objects.create(title=title, content=content, teacher=teacher)

            for group_id in group_ids:
                try:
                    group = Group.objects.get(id=group_id)
                    lesson.groups.add(group)
                except Group.DoesNotExist:
                    return Response({"error": f"Group ID {group_id} topilmadi!"}, status=status.HTTP_404_NOT_FOUND)

            lesson.save()

            return Response({
                "id": lesson.id,
                "title": lesson.title,
                "content": lesson.content,
                "groups": [group.id for group in lesson.groups.all()],
                "teacher": lesson.teacher.id
            }, status=status.HTTP_201_CREATED)

        except Teacher.DoesNotExist:
            return Response({"error": "Bunday teacher mavjud emas!"}, status=status.HTTP_404_NOT_FOUND)

class TeacherListView(generics.ListAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

class StudentListView(generics.ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class GroupListView(generics.ListAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class LessonListAPIView(generics.ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

class AddLessonToGroupAPIView(APIView):
    def post(self, request):
        lesson_id = request.data.get("lesson_id")
        group_name = request.data.get("group_name")

        if not lesson_id or not group_name:
            return Response({"error": "lesson_id va group_name kerak!"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            lesson = Lesson.objects.get(id=lesson_id)
            group = Group.objects.get(name=group_name)
        except Lesson.DoesNotExist:
            return Response({"error": "Bunday Lesson topilmadi!"}, status=status.HTTP_404_NOT_FOUND)
        except Group.DoesNotExist:
            return Response({"error": "Bunday Group topilmadi!"}, status=status.HTTP_404_NOT_FOUND)

        lesson.groups.add(group)
        return Response({"message": f"Lesson '{lesson.title}' guruh '{group.name}'ga qoshildi!"}, status=status.HTTP_200_OK)


class LessonGroupListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer

    def get_queryset(self):
        return Lesson.objects.filter(groups__isnull=False).distinct()
    
class DeleteTeacherAPIView(APIView):
    def delete(self, request):
        try:
            data = json.loads(request.body)
            teacher_id = data.get("id")

            teacher = Teacher.objects.get(id=teacher_id)

            groups = teacher.groups.all()
            for group in groups:
                group.teacher = None
                group.save()

            teacher.delete()
            return Response({"message": f"Teacher {teacher_id} ochirildi!"}, status=status.HTTP_200_OK)

        except Teacher.DoesNotExist:
            return Response({"error": "Bunday teacher mavjud emas!"}, status=status.HTTP_404_NOT_FOUND)
        except json.JSONDecodeError:
            return Response({"error": "Notogri JSON format!"}, status=status.HTTP_400_BAD_REQUEST)
        
class DeleteStudentAPIView(APIView):
    def delete(self, request):
        try:
            data = json.loads(request.body)
            student_id = data.get("id")

            student = Student.objects.get(id=student_id)
            student.delete()
            return Response({"message": f"Student {student_id} ochirildi!"}, status=status.HTTP_200_OK)

        except Student.DoesNotExist:
            return Response({"error": "Bunday student mavjud emas!"}, status=status.HTTP_404_NOT_FOUND)
        except json.JSONDecodeError:
            return Response({"error": "Notogri JSON format!"}, status=status.HTTP_400_BAD_REQUEST)
        
class DeleteGroupAPIView(APIView):
    def delete(self, request):
        try:
            data = json.loads(request.body)
            group_id = data.get("id")

            group = Group.objects.get(id=group_id)
            group.delete()
            return Response({"message": f"Group {group_id} ochirildi!"}, status=status.HTTP_200_OK)

        except Group.DoesNotExist:
            return Response({"error": "Bunday group mavjud emas!"}, status=status.HTTP_404_NOT_FOUND)
        except json.JSONDecodeError:
            return Response({"error": "Notogri JSON format!"}, status=status.HTTP_400_BAD_REQUEST)
        
class DeleteLessonAPIView(APIView):
    def delete(self, request):
        try:
            data = json.loads(request.body)
            lesson_id = data.get("id")

            lesson = Lesson.objects.get(id=lesson_id)
            lesson.delete()
            return Response({"message": f"Lesson {lesson_id} ochirildi!"}, status=status.HTTP_200_OK)

        except Lesson.DoesNotExist:
            return Response({"error": "Bunday lesson mavjud emas!"}, status=status.HTTP_404_NOT_FOUND)
        except json.JSONDecodeError:
            return Response({"error": "Notogri JSON format!"}, status=status.HTTP_400_BAD_REQUEST)
        
class GroupListAPIView(ListAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
        

class AddStudentToGroupAPIView(APIView):
    def post(self, request, *args, **kwargs):
        group_id = request.data.get("group_id")
        student_id = request.data.get("student_id")

        if not group_id or not student_id:
            return Response({"error": "group_id va student_id kerak"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            group = Group.objects.get(id=group_id)
            student = Student.objects.get(id=student_id)
            group.students.add(student)
            return Response({"message": "Student groupga qoshildi"}, status=status.HTTP_200_OK)
        except Group.DoesNotExist:
            return Response({"error": "Group topilmadi"}, status=status.HTTP_404_NOT_FOUND)
        except Student.DoesNotExist:
            return Response({"error": "Student topilmadi"}, status=status.HTTP_404_NOT_FOUND)

class RemoveStudentFromGroupAPIView(APIView):
    def post(self, request):
        group_id = request.data.get("group_id")
        student_id = request.data.get("student_id")

        try:
            group = Group.objects.get(id=group_id)
            student = Student.objects.get(id=student_id)
            group.students.remove(student)
            return Response({"message": "Student groupdan ochirildi"}, status=status.HTTP_200_OK)
        except Group.DoesNotExist:
            return Response({"error": "Group topilmadi"}, status=status.HTTP_404_NOT_FOUND)
        except Student.DoesNotExist:
            return Response({"error": "Student topilmadi"}, status=status.HTTP_404_NOT_FOUND)