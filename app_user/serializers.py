from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from app_user.models import Student, Group, Teacher, TeacherGroup, Lesson 


User = get_user_model()


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['id', 'name']




class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        data.update({
            "user_id": self.user.id,
            "username": self.user.username,
            "email": self.user.email,
            "is_staff": self.user.is_staff,
            "is_superuser": self.user.is_superuser,
        })

        return data


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['id', 'name']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        teacher = Teacher.objects.create(**validated_data)
        return teacher

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'name', 'age']

class GroupSerializer(serializers.ModelSerializer):
    students = StudentSerializer(many=True, read_only=True)

    class Meta:
        model = Group
        fields = ['id', 'name', 'students']


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
        lesson.groups.set(groups_data) 
        return lesson