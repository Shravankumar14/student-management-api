from django.shortcuts import get_object_or_404

from rest_framework import status, generics, filters
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser
)
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet

from django_filters.rest_framework import DjangoFilterBackend

from .models import Student
from .serializers import (
    StudentSerializer,
    UserRegisterSerializer
)

from .permissions import (
    CanDeleteOnlyECEStudent
)

from rest_framework_simplejwt.tokens import RefreshToken

from .permissions import IsAdminOrReadOnly

from rest_framework.viewsets import ModelViewSet

from .models import Student, Course
from .serializers import StudentSerializer, CourseSerializer

from .permissions import CanDeleteOnlyECEStudent



@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def student_list(request):

    if request.method == 'GET':

        branch = request.GET.get('branch')
        search = request.GET.get('search')
        ordering = request.GET.get('ordering')

        students = Student.objects.all()

        if branch:
            students = students.filter(branch=branch)

        if search:
            students = students.filter(
                name__icontains=search
            )

        if ordering:
            students = students.order_by(ordering)

        paginator = PageNumberPagination()
        paginator.page_size = 2

        result_page = paginator.paginate_queryset(
            students,
            request
        )

        serializer = StudentSerializer(
            result_page,
            many=True
        )

        return paginator.get_paginated_response(
            serializer.data
        )

    serializer = StudentSerializer(
        data=request.data
    )

    if serializer.is_valid():
        serializer.save()

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def student_detail(request, pk):

    student = get_object_or_404(
        Student,
        pk=pk
    )

    if request.method == 'GET':
        serializer = StudentSerializer(student)

        return Response(serializer.data)

    elif request.method == 'PUT':

        serializer = StudentSerializer(
            student,
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    student.delete()

    return Response(
        {
            "message":
            "Student deleted successfully"
        },
        status=status.HTTP_204_NO_CONTENT
    )


class StudentListView(
    generics.ListCreateAPIView
):

    queryset = Student.objects.all()

    serializer_class = StudentSerializer

    permission_classes = [IsAuthenticated]

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]

    filterset_fields = ['branch']

    search_fields = ['name']

    ordering_fields = [
        'name',
        'age'
    ]


class StudentDetailView(
    generics.RetrieveUpdateDestroyAPIView
):

    queryset = Student.objects.all()

    serializer_class = StudentSerializer

    permission_classes = [IsAuthenticated]



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_user(request):

    try:

        refresh_token = request.data["refresh"]

        token = RefreshToken(refresh_token)

        token.blacklist()

        return Response(
            {"message": "Logout successful"},
            status=status.HTTP_205_RESET_CONTENT
        )

    except Exception as e:

        return Response(
            {"error": "Invalid token"},
            status=status.HTTP_400_BAD_REQUEST
        )

def register_user(request):

    serializer = UserRegisterSerializer(
        data=request.data
    )

    if serializer.is_valid():
        serializer.save()

        return Response(
            {
                "message":
                "User created successfully"
            },
            status=status.HTTP_201_CREATED
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )


class StudentViewSet(ModelViewSet):

    queryset = Student.objects.all()

    serializer_class = StudentSerializer

    permission_classes = [IsAdminOrReadOnly]

    def get_permissions(self):

        if self.action == 'destroy':

            return [
                IsAdminUser(),
                CanDeleteOnlyECEStudent()
            ]

        if self.action in [
            'update',
            'partial_update'
        ]:

            return [IsAdminUser()]

        return [IsAuthenticated()]

    def get_object(self):
        obj = super().get_object()

        self.check_object_permissions(
            self.request,
            obj
        )

        return obj
    

class CourseViewSet(ModelViewSet):

    queryset = Course.objects.all()

    serializer_class = CourseSerializer

    permission_classes = [IsAuthenticated]


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile(request):

    return Response({
        "id": request.user.id,
        "username": request.user.username,
        "email": request.user.email,
    })

