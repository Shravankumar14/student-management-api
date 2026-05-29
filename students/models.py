from django.db import models


class Course(models.Model):

    name = models.CharField(max_length=100)

    duration = models.IntegerField()

    def __str__(self):

        return self.name


class Student(models.Model):

    name = models.CharField(max_length=100)

    age = models.IntegerField()

    branch = models.CharField(max_length=50)

    photo = models.ImageField(
        upload_to='students/',
        null=True,
        blank=True
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='students',
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name