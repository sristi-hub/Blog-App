from django.db import models
from account.models import User
from posts.models import Post

# Create your models here.
class PostLike(models.Model):
    post = models.ForeignKey(Post, on_delete= models.CASCADE, related_name= "likes")
    user = models.ForeignKey(User, on_delete= models.CASCADE, related_name = "mylikes")
    is_active = models.BooleanField(default = True)
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now= True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields = ['post', 'user'], name = "unique_post_like")
        ]
