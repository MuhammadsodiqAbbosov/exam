from rest_framework import serializers
from .models import Teacher
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
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


