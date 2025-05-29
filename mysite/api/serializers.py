# It converts the python class object into JSON format
# Serializer is a class that takes the model class and convert the model into JSON

from rest_framework import serializers
from django.contrib.auth.models import User

from blogposts.models import BlogPost
from employees.models import Employee

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email"]

class BlogPostSerializer(serializers.ModelSerializer):
    author = UserSerializer()

    class Meta:
        model = BlogPost
        fields = ["id", "title", "content", "published_date", "updated_at", "author"] # OR, fields = "__all__"


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'

        # When you define a method in the form of `validate_<field_name>`, DRF automatically uses it to validate that specific field.
        # value = emp_id
        def validate_emp_id(self, value):

            if self.instance:  # This means it's an update, not creation
                if Employee.objects.filter(emp_id=value).exclude(id=self.instance.id).exists():
                    raise serializers.ValidationError('Employee with same id exists')

            if Employee.objects.filter(emp_id=value).exists():
                raise serializers.ValidationError('Employee with same id exists')

            return value
