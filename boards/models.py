from django.db    import models
from users.models import Profile

class BoardCategory(models.Model):
    name = models.CharField(max_length=32)

    class Meta:
        db_table = "board_categories"

class Board(models.Model):
    author     = models.ForeignKey(Profile,on_delete=models.CASCADE)
    title      = models.CharField(max_length=128)
    content    = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    views      = models.IntegerField(default=0)
    category   = models.ForeignKey('BoardCategory',on_delete=models.SET_NULL,null=True)

    class Meta:
        db_table = "boards"

class Comment(models.Model):
    author     = models.ForeignKey(Profile,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)
    board      = models.ForeignKey('Board',on_delete=models.CASCADE)
    content    = models.CharField(max_length=256)
    
    class Meta:
        db_table = "comments"

class Appendix(models.Model):
    urls      = models.CharField(max_length=100)
    filename  = models.CharField(max_length=100)
    board     = models.ForeignKey('Board',on_delete=models.CASCADE)

    class Meta:
        db_table = "appendixs"

