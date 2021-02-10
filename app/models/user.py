from django.db import models


class User(models.Model):
    user_name = models.CharField(max_length=50, primary_key=True)
    password = models.CharField(max_length=100)
    email = models.EmailField()
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now_add=True)
