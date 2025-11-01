from django.db import models
from account.models import User
from posts.models import Post
from django.utils import timezone

# Create your models here.
class Comment(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    )

    content = models.TextField(blank = True)
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'my_comments')
    post = models.ForeignKey(Post, on_delete = models.CASCADE, related_name = 'all_comments')
    parent = models.ForeignKey('self', null = True, blank = True, on_delete = models.CASCADE, related_name = 'replies')
    created_at = models.DateTimeField(auto_now_add = True) #set once when created
    updated_at = models.DateTimeField(auto_now = True)   #Updates on every save
    status = models.CharField(max_length= 10, choices = STATUS_CHOICES, default = 'approved')

   
    def __str__(self):
        return f'Comment by {self.user.full_name} to the post {self.post.title}'