# It converts the python class object into JSON format
# Serializer is a class that takes the model class and convert the model into JSON

from rest_framework import serializers
from .models import BlogPost

class BlogPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = ["id", "title", "content", "published_date"]