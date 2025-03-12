from rest_framework import serializers
from .models import Teacher
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
User = get_user_model()


from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Teacher  

User = get_user_model()  # Django default user modelini olish

class TeacherSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ( 'id', 'name', 'user', 'role', 'created_at', 'updated_at')

    def create(self, validated_data):
        role = validated_data.pop("role", None)  # Role ni ajratib olish
        user = User.objects.create_user(**validated_data)  # User yaratish
        if role:
            user.role = role  # Role ni 
            if user.role == 'admin': 
                user.is_staff = True
                user.is_superuser = True

            user.save()
        return user



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


