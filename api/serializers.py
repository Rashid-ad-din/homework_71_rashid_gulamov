from rest_framework import serializers

from posts.models import Comments, Post


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ('id', 'author', 'post', 'text')


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = (
            'id',
            'description',
            'image',
            'author',
            'is_deleted',
            'created_at',
            'updated_at',
            'deleted_at',
        )
        read_only_fields = (
            'id',
            'author',
            'is_deleted',
            'created_at',
            'updated_at',
            'deleted_at',
        )

    def update(self, instance, validated_data):
        instance.description = validated_data.get('description')
        instance.image = validated_data.get('image', instance.image)
        instance.save()
        return instance

    def create(self, validated_data, author=None):
        post = Post.objects.create(**validated_data, author=self.author)
        return post
