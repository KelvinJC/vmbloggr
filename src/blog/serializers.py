from rest_framework import serializers
from .models import BlogPost
from users.models import User


# class BlogPostSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = BlogPost
#         fields = [
#             'author',
#             'title',
#             'subtitle',
#             'body',
#             'date_created',
#         ]

#     user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())


class BlogPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = '__all__'

class BlogPostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = ['title', 'subtitle', 'body']

    def create(self, validated_data):
        # Add the current user as the author of the blog post
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)
    
class AllBlogPostsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = '__all__'
    
    def to_representation(self, post):
        # Check if post is a list (i.e. all records) or a single instance (one record)
        is_list = isinstance(post, list)
        if is_list:
            # Serialize all records
            return super(AllBlogPostsSerializer, self).to_representation(post)
        else:
            # Serialize a single record
            return BlogPostSerializer(post).data
