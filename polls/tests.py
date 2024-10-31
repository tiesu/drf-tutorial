from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from polls.models import Post


class PostAPITestCase(APITestCase):
    def setUp(self):
        # 관리자 사용자 생성
        self.admin_user = User.objects.create_superuser(username='admin', password='admin123')

        refresh = RefreshToken.for_user(self.admin_user)
        self.access_token = str(refresh.access_token)

    def test_create_post(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        data = {
            'title': 'Test Post',
            'content': 'Test Post Content',
            'author': 'admin',
        }

        response = self.client.post('/polls/posts/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class PostOwnerTestCase(APITestCase):
    def setUp(self):
        # 두 명의 사용자 생성
        self.user1 = User.objects.create_user(username='user1', password='password123')
        self.user2 = User.objects.create_user(username='user2', password='password123')

        refresh = RefreshToken.for_user(self.user1)
        self.access_token = str(refresh.access_token)

        self.content = Post.objects.create(title='User1 Post', author='user1', content='User1 Post Content')

    def test_owner_can_update(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        data = {
            'title': 'Updated Title',
            'content': 'Updated Content',
            'author': 'user1',
        }
        response = self.client.put(f'/polls/posts/{self.content.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_other_user_cannot_update(self):
        refresh = RefreshToken.for_user(self.user2)
        self.access_token = str(refresh.access_token)

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        data = {
            'title': 'Updated Title',
            'content': 'Updated Content',
            'author': 'user1',
        }
        response = self.client.put(f'/polls/posts/{self.content.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)