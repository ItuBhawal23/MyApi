from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# <app_label>_<model_name> #table name created in db (blogposts_blogpost)

class BlogPost(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE) # on_delete- if user is deleted (all blogs associated with the user will be deleted)

    class Meta:
        db_table = 'blogposts'

    def __str__(self):
        return self.title