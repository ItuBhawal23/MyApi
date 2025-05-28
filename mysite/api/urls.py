from django.urls import path
from . import views

urlpatterns =[
    path("blogposts/", views.BlogPostListCreateView.as_view(), name='blogpost_view_create'),
    path("blogposts/<int:pk>", views.BlogPostRetrieveUpdateDestroyView.as_view(), name='update_delete_retrieve')
]