from django.db import models

class User(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 

class Job(models.Model):
    title = models.CharField(max_length = 255)
    users = models.ManyToManyField(User, related_name="has_jobs")
    post_by = models.ForeignKey(User, related_name='posted')
    desc = models.TextField()
    category = models.CharField(max_length = 255)
    location = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 