from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from users.models import User  
from django.urls import reverse


class UserCreateViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.valid_user_data = {
            "username": "testuser",
            "password": "testpassword",
            'email': 'username@gmail.com', 
            'phone_number': 1232434353343
        }

    def test_create_user(self):
        response = self.client.post('/api/users/user/', self.valid_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_user_missing_required_field(self):
        # Remove the 'username' field to make the request invalid
        invalid_data = self.valid_user_data.copy()
        invalid_data.pop('username')
        response = self.client.post('/api/users/user/', invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_existing_email(self):
        # Create a user with the same email
        User.objects.create_user(username="existinguser", password="password", email=self.valid_user_data['email'])

        response = self.client.post('/api/users/user/', self.valid_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_existing_phone_number(self):
        # Create a user with the same phone number
        User.objects.create_user(username="existinguser", password="password", email=self.valid_user_data['email'], phone_number=self.valid_user_data['phone_number'])

        response = self.client.post('/api/users/user/', self.valid_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_new_phone_number(self):
        # Create a user with new phone number
        User.objects.create_user(username="existinguser", password="password", email="ab@gmail.com", phone_number=1232434354444)

        response = self.client.post('/api/users/user/', self.valid_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class UserViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(username="testuser1", password="testpassword1", email='er@gmail.com', phone_number=323433245344)
        self.client.force_authenticate(user=self.user)

    # def test_destroy_user(self):
    #     response = self.client.delete(f'/api/users/{self.user.id}/')
    #     self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_destroy_user_permission_denied(self):
        other_user = User.objects.create(username="otheruser", password="otherpassword")
        self.client.force_authenticate(user=other_user)  # Simulate a different user
        response = self.client.delete(f'/api/users/{self.user.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_single_user(self):
        response = self.client.get(f'/api/users/{self.user.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # # For now all users can view a user's user info
    # def test_retrieve_single_user_permission_denied(self):
    #     other_user = User.objects.create(username="otheruser", password="otherpassword")
    #     response = self.client.get(f'/api/users/{other_user.id}/')  # Try to access another user's user
    #     self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_all_users(self):
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # # For now all users can view list of all users info
    # def test_retrieve_all_users_permission_denied(self):
    #     other_user = User.objects.create(username="otheruser", password="otherpassword")
    #     self.client.force_authenticate(user=other_user)  # Simulate a different user
    #     response = self.client.get('/api/users/')  # Try to retrieve all users
    #     self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_update_user(self):
        updated_data = {
            "username": "newusername",
            "email": "newemail@example.com",
            "phone_number": 1234567890
        }
        response = self.client.put(f'/api/users/{self.user.id}/', updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, "newusername")
        self.assertEqual(self.user.email, "newemail@example.com")
        self.assertEqual(self.user.phone_number, '1234567890')

    def test_update_user_permission_denied(self):
        other_user = User.objects.create(username="otheruser", password="otherpassword")
        self.client.force_authenticate(user=other_user)  # Simulate a different user
        updated_data = {
            "username": "newusername",
            "email": "newemail@example.com",
            "phone_number": 1234567890
        }
        response = self.client.put(f'/api/users/{self.user.id}/', updated_data, format='json')  # Try to update another user's user
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_user(self):
        updated_data = {
            "email": "newemail@example.com"
        }
        response = self.client.patch(f'/api/users/{self.user.id}/', updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, "newemail@example.com")

    def test_patch_user_permission_denied(self):
        other_user = User.objects.create(username="otheruser", password="otherpassword")
        self.client.force_authenticate(user=other_user)  # Simulate a different user
        updated_data = {
            "email": "newemail@example.com"
        }
        response = self.client.patch(f'/api/users/{self.user.id}/', updated_data, format='json')  # Try to patch another user's user
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class LoginAPIViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            "username": "testuser",
            "password": "testpassword"
        }
        self.invalid_user_data = {
            "username": "testuser",
            "password": "invalidpassword"
        }

        # Create a user for testing
        self.user = User.objects.create_user(**self.user_data)

    def test_valid_login(self):
        url = reverse('token_obtain_pair')
        response = self.client.post(url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_invalid_login(self):
        url = reverse('token_obtain_pair')
        response = self.client.post(url, self.invalid_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
