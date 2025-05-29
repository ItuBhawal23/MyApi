from django.core.serializers import serialize
from django.http import HttpResponse, JsonResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.template.context_processors import request
from rest_framework import generics, status, mixins, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import BlogPostSerializer, EmployeeSerializer
from blogposts.models import BlogPost
from employees.models import Employee

# DRF features - request parsing, authentication, and response rendering.
# Create your views here.


# Manual serializer without DRF
# def blog_post_view(request):
#         blog_posts = BlogPost.objects.all() #blog_post = queryset
#
#         #manual serialize -> convert the quertset to `list`
#         blog_post_list = list(blog_posts.values())
#         return JsonResponse(blog_post_list, safe=False) #JsonResp(dic_obj) if not => safe=False



# function-based view using serializer
"""
@api_view Decorator that converts a function-based view into an APIView subclass & return REST framework responses.
Takes a list of allowed methods for the view as an argument.
"""
@api_view(['GET', 'POST'])
def blog_posts_view(request):
        if request.method == 'GET':
                blog_posts = BlogPost.objects.all() # model instances retrieved from the database.

                # DRF serializer method - creates a serializer instance
                # When you pass model instances directly, you don’t need to use data=
                serializer = BlogPostSerializer(blog_posts, many=True)

                return Response(serializer.data, status=status.HTTP_200_OK) # serializer.data extracts the serialized (JSON-ready) data.

        elif request.method == 'POST':
                 #data= is used here because the user input is deserialized before saving
                serializer = BlogPostSerializer(data=request.data) #initializes the serializer with request data

                if serializer.is_valid(): #in-built validation checks
                        serializer.save() #insert it into the DB.
                        return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({'detail': 'Method not allowed.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


# function-based view to get fetch single object (pk based)
@api_view(['GET', 'PUT', 'DELETE'])
def blog_post_view(request, pk):
        try:
                blogpost = BlogPost.objects.get(pk=pk)
        except:
                return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
                serializer = BlogPostSerializer(blogpost)
                return Response(serializer.data, status=status.HTTP_200_OK)

        elif request.method == 'PUT':
                serializer = BlogPostSerializer(blogpost, request.data)

                if serializer.is_valid():
                        serializer.save()
                        return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                        return Response(status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
                blogpost.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)

        else:
                return Response({'detail': 'Method not allowed.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)



'''
# Class Based View
It provides more structured & organized way to handle requests using Object-oriented principles
It takes away the conditional checks based on the request (in function-based view)
Here we can use instance methods like get(), post(), put(), delete() which will be mapped accordingly
'''

class Employees(APIView):
        # member funcs of this class
        def get(self, request):
                employees = Employee.objects.all()
                serializer = EmployeeSerializer(employees, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)

        def post(self, request):
                serializer = EmployeeSerializer(data=request.data)

                if serializer.is_valid():
                        serializer.save()
                        return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(status=status.HTTP_400_BAD_REQUEST)

class EmployeeDetail(APIView):

        # get the employee based on pk
        def get_employee(self, pk):
                try:
                        return Employee.objects.get(pk=pk)
                except:
                        return Http404

        def get(self, request, pk):
                employee = self.get_employee(pk)
                serializer = EmployeeSerializer(employee)
                return Response(serializer.data, status=status.HTTP_200_OK)

        def put(self, request, pk):
                employee = self.get_employee(pk)
                serializer = EmployeeSerializer(employee, data=request.data)

                if serializer.is_valid():
                        serializer.save()
                        return Response(serializer.data, status=status.HTTP_200_OK)
                return Response(status=status.HTTP_400_BAD_REQUEST)


        def delete(self, request, pk):
                employee = self.get_employee(pk)
                employee.delete()

                return Response(status=status.HTTP_404_NOT_FOUND)


'''
MIXINS In DRF:
Mixins are reusable classes that provide common functionality for views
'''

class EmployeesMixin(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
        queryset = Employee.objects.all()
        serializer_class = EmployeeSerializer

        def get(self, request):
                return self.list(request)

        def post(self, request):
                return self.create(request)



class EmployeeDetailMixin(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
        queryset = Employee.objects.all()
        serializer_class = EmployeeSerializer

        def get(self, request, pk):
                return self.retrieve(request, pk)

        def put(self, request, pk):
                return self.update(request, pk)

        def delete(self, request, pk):
                return self.destroy(request, pk)




'''
class-based view using generic from DRF
Generics - pre-built view classes & mixins that encapsulate the common API functionalities for CURD Oper.
         - avoids writing of get(), put(), post() etc for CURD Oper., reduces the boiler plate code
         - It has single APIView and combinations of APIView for CURD Oper.
         - Required - queryset, serializer_class, lookup_field?
'''

# List [GET], Create [POST]
# class BlogPostListCreateView(generics.ListAPIView, generics.CreateAPIView):
class BlogPostListCreateView(generics.ListCreateAPIView):
        queryset = BlogPost.objects.all()
        serializer_class = BlogPostSerializer


# retrieve[GET], Update [PUT/PATCH], Destroy [DELETE] by PrimaryKey(id) operations
# class BlogPostRetrieveUpdateDestroyView(generics.RetrieveAPIView, generics.UpdateAPIView, generics.DestroyAPIView):
class BlogPostRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
        # querySet is lazy, chainable, iterable object returned by model manager
        queryset = BlogPost.objects.all()
        serializer_class = BlogPostSerializer
        lookup_field = "pk" #primary_key

        # delete all
        def delete(self, request, *args, **kwargs):
                BlogPost.objects.all().delete()
                return Response(status=status.HTTP_204_NO_CONTENT)




# APIView = base class for all class-based views(get, post,put,delete) | custom API logic
# This logic allows searching blog posts by `title` using a query parameter.
# Without it: You’d always return all blog posts, even if the user wants to search by query.

class BlogPostList(APIView):

        def get(self, request, format=None):

                # Get the title from the query parameters (if none, default to string)
                # /api/blogposts/?title=django
                # title = "django"
                title = request.query_params.get("title", "")
                # published_date = request.query_params("published_date", "") # other fields can also be filtered based on user requested query params

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
                return Response(serializer.data, status=status.HTTP_200_OK)



# ViewSets - one class that handles all crud operations and its respective urls

# viewsets.ViewSet => It provides in-built methods to perform CURD Ope. list(), create(), retrieve(), update(), delete()
# A single viewset class method, as the url is handled by DRF router
class EmployeesViewSet(viewsets.ViewSet):
        def list(self, request):
                queryset = Employee.objects.all()
                serializer = EmployeeSerializer(queryset, many=True)

                return Response(serializer.data, status=status.HTTP_200_OK)


        def create(self, request):
                serializer = EmployeeSerializer(data=request.data)

                if serializer.is_valid():
                        serializer.save()
                        return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(status=status.HTTP_400_BAD_REQUEST)


        def retrieve(self, request, pk):
                employee = get_object_or_404(Employee, pk=pk) # django shortcuts method

                serializer = EmployeeSerializer(employee)
                return Response(serializer.data, status=status.HTTP_200_OK)

        def update(self,request, pk):
                employee = get_object_or_404(Employee, pk=pk)

                serializer = EmployeeSerializer(employee, data=request.data)
                if serializer.is_valid():
                        return Response(serializer.data, status=status.HTTP_200_OK)
                return Response(status=status.HTTP_400_BAD_REQUEST)


        def delete(self, request, pk):
                employee = get_object_or_404(Employee, pk=pk)

                employee.delete()
                return Response(status=status.HTTP_404_NOT_FOUND)


# viewsets.ModalViewSet
# queryset
# Automatic serialization (serializer_class)
# Automatic determine the url from the router

class EmpViewSet(viewsets.ModelViewSet):
        queryset = Employee.objects.all()
        serializer_class = EmployeeSerializer