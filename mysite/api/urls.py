from django.db import router
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
# router.register('emps', views.EmployeesViewSet, basename='emp')
router.register('emps', views.EmpViewSet, basename='emp')

urlpatterns =[
    # function-based view
    path("blogposts/", views.blog_posts_view, name='blogpost_view_create'),
    path('blogposts/<int:pk>/', views.blog_post_view, name='blog_post_view'),

    # as_view() is added when views is class-based

    # class-based view with generics.APIView
    # path('employees/', views.Employees.as_view(), name='employees'),
    # path('employees/<int:pk>/', views.EmployeeDetail.as_view(), name='employee_detail'),

    # class-based-view using mixins & GenericAPIView from DRF
    path('employees/', views.EmployeesMixin.as_view(), name='employees'),
    path('employees/<int:pk>/', views.EmployeeDetailMixin.as_view(), name='employee_detail'),

    # generic class-based view
    # path("blogposts/", views.BlogPostListCreateView.as_view(), name='blogpost_view_create'),
    # path("blogposts/<int:pk>", views.BlogPostRetrieveUpdateDestroyView.as_view(), name='update_delete_retrieve')

    # APIView
    # path("blogposts/", views.BlogPostList.as_view(), name='blogpost_view_create'),

    # router view
    path('', include(router.urls))
]