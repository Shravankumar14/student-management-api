from rest_framework import serializers
from .models import Student,Course

from django.contrib.auth.models import User



class StudentMiniSerializer(serializers.ModelSerializer):

    class Meta:
        model = Student
        fields = ['id', 'name']


class CourseSerializer(serializers.ModelSerializer):

    students = StudentMiniSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = Course
        fields = [
            'id',
            'name',
            'duration',
            'students'
        ]

class StudentSerializer(serializers.ModelSerializer):

    course_details = CourseSerializer(
        source='course',
        read_only=True
    )

    class Meta:

        model = Student

        fields = [
            'id',
            'name',
            'age',
            'branch',
            'photo',
            'course',
            'course_details'
        ]


class UserRegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user 
    


