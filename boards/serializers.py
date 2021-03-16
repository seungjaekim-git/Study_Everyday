from rest_framework import serializers
from boards.models  import Board, Comment, BoardCategory, Appendix
from users.serializers   import UserDetailSerializer

class CommentSerializer(serializers.ModelSerializer):
    
    author = UserDetailSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ('id','author', 'created_at','updated_at','content')

class BoardCateogrySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = BoardCategory
        fields = ('id','name')

class AppendixSerializer(serializers.ModelSerializer):

    class Meta:
        model = Appendix
        fields = ('id','filename')

class BoardSerializer(serializers.ModelSerializer):
    
    category = BoardCateogrySerializer(read_only=True)
    author = UserDetailSerializer(read_only=True)
    appendix = AppendixSerializer(read_only=True,many=True)
    comment = CommentSerializer(read_only=True,many=True)

    class Meta:
        model = Board
        fields = ('id', 'title', 'author', 'content', 'created_at', 'updated_at', 'views','comment','appendix')



