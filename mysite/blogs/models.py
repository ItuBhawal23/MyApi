from django.db import models

# Create your models here.

class Blog(models.Model):
    blog_title = models.CharField(max_length=100)
    blog_body = models.TextField()

    class Meta:
        db_table = 'blog'

    # string representation of blog model
    def __str__(self):
        return self.blog_title

# 1 blog = Many comments
class Comment(models.Model):
    comment = models.CharField(max_length=200)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return self.comment


'''
blogs = Blogs.objects.all()
blogs.comments.all() # Returns all comments objects linked to this blog
'''