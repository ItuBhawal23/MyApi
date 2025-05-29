from django.db import models

# Create your models here.

class Employee(models.Model):
    emp_id = models.CharField(max_length=500, unique=True)
    emp_name = models.CharField(max_length=50)
    designation = models.CharField(max_length=100)

    def __str__(self):
        return self.emp_name