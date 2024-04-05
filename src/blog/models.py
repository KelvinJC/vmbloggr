from django.db import models
from users.models import User

class BlogPostModelManager(models.Manager):
    
    def delete(self, id):
        ''' delete a single blog post'''
        blog = self.get(pk=id)
        if (not blog.is_deleted):
            blog.is_deleted = True
        return
        
    def get_all(self):
        ''' get all blog posts'''
        query = self.get_queryset()
        return query.filter(blogpost__is_deleted=False)
    
    def get(self, id):
        ''' get a single blog post '''
        return self.get(pk=id)
    
    def find_by_author(self, author_id):
        ''' search for all blog posts by a common author'''
        pass

    

class BlogPost(models.Model):

    title = models.TextField(null=True, blank=True)
    subTitle = models.TextField(null=True, blank=True)
    body = models.TextField(null=True, blank=True)
    dateCreated = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='author')
    is_deleted = models.BooleanField(default=False)

    objects = BlogPostModelManager()

    def __repr__(self) -> str:
        return self.title