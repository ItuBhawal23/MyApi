from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import BlogPost
from .serializers import BlogPostSerializer


# Create your views here.


# class-based view

# List [GET], Create [POST]
class BlogPostListCreateView(generics.ListCreateAPIView):
        queryset = BlogPost.objects.all()
        serializer_class = BlogPostSerializer


# retrieve[GET], Update [PUT/PATCH], Destroy [DELETE] by PrimaryKey(id) operations
class BlogPostRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
        # querySet is lazy, chainable, iterable object returned by model manager
        queryset = BlogPost.objects.all()
        serializer_class = BlogPostSerializer
        lookup_field = "pk" #primary_key

        def delete(self, request, *args, **kwargs):
                BlogPost.objects.all().delete()
                return Response(status=status.HTTP_204_NO_CONTENT)


# DRF features - request parsing, authentication, and response rendering.

# APIView = base class for all class-based views | custom API logic
# This logic allows searching blog posts by `title` using a query parameter.
# Without it: You’d always return all blog posts, even if the user wants to search by query.

class BlogPostList(APIView):

        def get(self, request, format=None):

                # Get the title from the query parameters (if none, default to string)
                # /api/blogposts/?title=django
                # title = "django"
                title = request.query_params.get("title", "")
                published_date = request.query_params("published_date", "") # other fields can also be filtered based on user requested query params

                if(title):
                        # if title, filter the queryset based on the title
                        # it finds all blog posts where the title contains the search word.
                        blog_post = BlogPost.objects.filter(title__icontains=title) # title__icontains (CASE SENSITIVE)- Django ORM lookup

                else:
                        # if no title is provided, return all blogs
                        # /api/blogposts/
                        # → title = ""(default)
                        blog_post = BlogPost.objects.all()


                serializer = BlogPostSerializer(blog_post, many=True) # manually serialize
                return Response(serializer, status=status.HTTP_200_OK)