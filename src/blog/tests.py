from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .models import BlogPost
from blog.models import BlogPost
from .serializers import BlogPostSerializer, AllBlogPostsSerializer
from users.models import User  

class BlogPostAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Create a user for testing
        self.author = User.objects.create(
            username="testuser1", 
            password="testpassword1", 
            email='er@gmail.com', 
            phone_number="+23407033795721"
        )
        self.other_user = User.objects.create(
            username="testuser3", 
            password="testpassword", 
            email='user3@gmail.com', 
            phone_number="+23307044795721"
        )
        # Create some BlogPost instances for testing
        self.blog1 = BlogPost.objects.create(
            author=self.author,
            title = "Some title",
            subtitle = "Some subtitle",
            body ="Some body :) haha.",
        )

        self.blog2 = BlogPost.objects.create(
            author=self.author,
            title = "Some second title",
            subtitle = "Some second subtitle",
            body ="Some second body :) haha.",
        )
        

    def test_list_blog_posts_user_authenticated(self):
        self.client.force_authenticate(user=self.author)
        url = reverse('blog-posts-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_list_blog_posts_user_not_authenticated(self):
        url = reverse('blog-posts-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_list_blog_posts_api_response_match_db(self):
        self.client.force_authenticate(user=self.author)
        url = reverse('blog-posts-list')
        response = self.client.get(url)
        api_blogs = response.data['results']

        # query list of blogs from the database
        db_blogs = BlogPost.objects.get_all().values('id', 'title', 'subtitle', 'body')

        # assert that number of blogs retrieved via API matches the number of blogs in the database
        self.assertEqual(len(api_blogs), db_blogs.count())

        # assert that each blog retrieved via API matches the corresponding blog from the database
        for api_blog, db_blog in zip(api_blogs, db_blogs):
            self.assertEqual(api_blog['id'], db_blog['id'])
            self.assertEqual(api_blog['title'], db_blog['title'])
            self.assertEqual(api_blog['subtitle'], db_blog['subtitle'])
            self.assertEqual(api_blog['body'], db_blog['body'])


    def test_list_blog_posts_fetches_only_undeleted_blog_posts(self):
        blog3 = BlogPost.objects.create(
            author=self.author,
            title = "Some third title",
            subtitle = "Some third subtitle",
            body ="Some third body :) haha.",
        )
        BlogPost.objects.delete(blog3.id) # delete only last blog post

        self.client.force_authenticate(user=self.author)
        url = reverse('blog-posts-list')
        response = self.client.get(url)
        api_blogs = response.data['results']

        # get the list of blogs directly from the database
        undeleted_db_blogs = BlogPost.objects.get_all().values('id', 'title', 'subtitle', 'body')

        # assert that the number of blogs retrieved via API matches the number of undeleted blogs in the database
        self.assertEqual(len(api_blogs), undeleted_db_blogs.count())

        # assert that each blog retrieved via API matches the corresponding blog from the database
        for api_blog, db_blog in zip(api_blogs, undeleted_db_blogs):
            self.assertEqual(api_blog['id'], db_blog['id'])
            self.assertEqual(api_blog['title'], db_blog['title'])
            self.assertEqual(api_blog['subtitle'], db_blog['subtitle'])
            self.assertEqual(api_blog['body'], db_blog['body'])


    def test_retrieve_blog_post_user_authenticated(self):
        self.client.force_authenticate(user=self.author)
        url = reverse('blog-post-detail', args=[self.blog1.id])
        serializer = AllBlogPostsSerializer(self.blog1)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('id'), serializer.data.get('id'))


    def test_retrieve_blog_post_user_not_authenticated(self):
        url = reverse('blog-post-detail', args=[self.blog1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_retrieve_blog_post_user_is_not_owner(self):
        another_author = User.objects.create(
            username="testuser2", 
            password="testpassword", 
            email='user2@gmail.com', 
            phone_number="+23407044795721"
        )
        self.client.force_authenticate(user=another_author)
        url = reverse('blog-post-detail', args=[self.blog1.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_update_blog_post_user_is_not_owner(self):
        # authenticate as another user
        self.client.force_authenticate(user=self.other_user)

        # attempt to update the blog post
        url = reverse('blog-post-detail', args=[self.blog1.id])
        updated_data = {'title': 'Updated Title', 'subtitle': 'Updated Subtitle', 'body': 'Updated Body'}
        response = self.client.put(url, updated_data, format='json')

        # assert that the update request is not allowed 
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # assert that the blog post data remains unchanged
        self.blog1.refresh_from_db()
        self.assertEqual(self.blog1.title, "Some title")
        self.assertEqual(self.blog1.subtitle, "Some subtitle")
        self.assertEqual(self.blog1.body, "Some body :) haha.")

    def test_partial_update_blog_post_user_is_not_owner(self):
        # authenticate as different user
        self.client.force_authenticate(user=self.other_user)

        # attempt to partially update the blog post
        url = reverse('blog-post-detail', args=[self.blog1.id])
        updated_data = {'title': 'Some title', 'subtitle': 'Some subtitle', 'body': 'Updated Body'}
        response = self.client.patch(url, updated_data, format='json')

        # assert that the partial update request is not allowed 
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # assert that the blog post data remains unchanged
        self.blog1.refresh_from_db()
        self.assertEqual(self.blog1.body, "Some body :) haha.")

    def test_delete_blog_post_user_is_not_owner(self):
        # authenticate as different user
        self.client.force_authenticate(user=self.other_user)

        # attempt to delete the blog post
        url = reverse('blog-post-detail', args=[self.blog1.id])
        response = self.client.delete(url)

        # assert that the delete request is not allowed 
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # assert that the blog post data remains unchanged
        self.blog1.refresh_from_db()
        self.assertEqual(self.blog1.title, "Some title")
        self.assertEqual(self.blog1.subtitle, "Some subtitle")
        self.assertEqual(self.blog1.body, "Some body :) haha.")


# TODO: 
# tEST CREATE ENDPOINT
# COMMIT CODE IN ORDER 'TRUST YOURSELF TO DETRMINE THE RIGHT ORDER'
# log your code
# create architecture diagram of app
# nginx, gunicorn, postgres, docker container
# log to std:out and document it as according to the 12 factor app

#####   print output of response.data   #####
# OrderedDict(
#     [
#         ('count', 2), 
#         ('next', None), 
#         ('previous', None), 
#         ('results', 
#             [
#                 OrderedDict(
#                     [
#                         ('id', 1), 
#                         ('title', 'Some title'), 
#                         ('subtitle', 'Some subtitle'), 
#                         ('body', 'Some body :) haha.'), 
#                         ('date_created', '2024-04-05T21:35:07.927089Z'), 
#                         ('is_deleted', False), 
#                         ('author', 1)
#                     ]
#                 ),
#                 OrderedDict(
#                     [
#                         ('id', 2), 
#                         ('title', 'Some second title'), 
#                         ('subtitle', 'Some second subtitle'), 
#                         ('body', 'Some second body :) haha.'), 
#                         ('date_created', '2024-04-05T21:35:07.927089Z'), 
#                         ('is_deleted', False), 
#                         ('author', 1)
#                     ]
#                 )
#             ]
        
#         )
#     ]
# )