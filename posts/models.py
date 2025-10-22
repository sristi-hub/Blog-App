from django.db import models
from account.models import User
from django.utils import timezone
# Create your models here.

class Category(models.Model) :
    name = models.CharField(max_length= 50, unique = True)
    description = models.TextField(blank = True)

    def __str__(self):
        return self.name
    
    
class Post(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published')

    ]

    title = models.CharField(max_length = 100)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'blogs')
    created_at = models.DateTimeField(default = timezone.now)
    updated_at = models.DateTimeField(auto_now = True)
    category = models.ForeignKey(Category, on_delete= models.CASCADE, related_name= 'posts')
    status = models.CharField(max_length = 10, choices = STATUS_CHOICES, default = 'draft')
    
    def __str__(self):
        return f'{self.title} by {self.author.full_name}'

    

