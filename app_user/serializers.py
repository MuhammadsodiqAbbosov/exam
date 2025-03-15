from rest_framework import serializers
from .models import Teacher
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
User = get_user_model()
from rest_framework import serializers
from .models import Teacher
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from .models import Teacher
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Teacher
from rest_framework import serializers
from .models import Teacher
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from .models import Student
from django.contrib.auth import get_user_model
from .models import Teacher
from rest_framework import serializers
from .models import Teacher
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from .models import Group
from .models import Teacher
from rest_framework import serializers
from app_user.models import TeacherGroup
from rest_framework import serializers
from .models import Teacher
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Teacher, Lesson

User = get_user_model()


from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Teacher  

User = get_user_model()  # Django default user modelini olish

from rest_framework import serializers
from .models import Teacher  

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['id', 'name']  # Faqat mavjud maydonlarni yozish kerak




class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        data.update({
            "user_id": self.user.id,
            "username": self.user.username,
            "email": self.user.email,
            "is_staff": self.user.is_staff,  # Agar admin bo‘lsa
            "is_superuser": self.user.is_superuser,  # Superuser yoki yo‘qligini tekshirish
        })

        return data


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['id', 'name']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        teacher = Teacher.objects.create(**validated_data)  # ✅ To‘g‘ri indentatsiya
        return teacher

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ('id', 'name', 'age', 'grade')


class GroupSerializer(serializers.ModelSerializer):
    lessons = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = ['id', 'name', 'lessons']

    def get_lessons(self, obj):
        lessons = obj.lessons.all()  # Ushbu groupdagi barcha lesson larni olish
        return LessonSerializer(lessons, many=True).data


class TeacherGroupSerializer(serializers.ModelSerializer):
    teacher_name = serializers.CharField(source="teacher.name", read_only=True)
    group_name = serializers.CharField(source="group.name", read_only=True)

    class Meta:
        model = TeacherGroup
        fields = ['id', 'teacher', 'teacher_name', 'group', 'group_name']

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'content', 'groups', 'teacher']

    def create(self, validated_data):
        groups_data = validated_data.pop('groups', [])
        lesson = Lesson.objects.create(**validated_data)
        lesson.groups.set(groups_data)  # Lessonni tanlangan gruppalarga bog'lash
        return lesson