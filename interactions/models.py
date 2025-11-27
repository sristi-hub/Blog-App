from django.db import models
from django.db.models import Q, F
from account.models import User
from posts.models import Post

# Create your models here.
class PostLike(models.Model):
    post = models.ForeignKey(Post, on_delete= models.CASCADE, related_name= "likes")
    user = models.ForeignKey(User, on_delete= models.CASCADE, related_name = "mylikes")
    is_active = models.BooleanField(default = True)
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now= True)

    def __str__(self):
        return f"{self.user.full_name} liked the post '{self.post.title}'"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields = ['post', 'user'], name = "unique_post_like")
        ]

class Bookmark(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE, related_name= 'bookmarks')
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'mybookmarks')
    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f"{self.user.full_name} bookmarked the post '{self.post.title}'"
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields = ['post', 'user'], name = "unique_user_post_bookmark")
        ]

class Follow(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE, related_name = 'following')
    author = models.ForeignKey(User, on_delete = models.CASCADE, related_name= 'followers')
    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f"{self.user.full_name} followed {self.author.full_name}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields = ['user', 'author'], name = "unique_user_author_follow"
                ),
            models.CheckConstraint(
                check = ~Q(user = F('author')),
                name = "prevent_self_follow"
            )
        ]