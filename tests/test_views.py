from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from Manager.models import *


class UserTests(APITestCase):

    def test_create_user(self):
        """
        Перевірка створення користувача.
        """
        url = reverse('create_user')
        data = {'username': 'testuser', 'password': 'password123'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'testuser')


class TagTests(APITestCase):

    def test_create_tag(self):
        """
        Перевірка створення тегу.
        """
        url = reverse('create_tag')
        data = {'name': 'Personal'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Tag.objects.count(), 1)
        self.assertEqual(Tag.objects.get().name, 'Personal')


class NoteTests(APITestCase):

    def setUp(self):
        # Створення користувача для тестів
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        # Створення тегу для тестів
        self.tag = Tag.objects.create(name='Test Tag')
        # Аутентифікація користувача перед тестуванням створення замітки
        self.client.force_authenticate(user=self.user)

    def test_create_note(self):
        """
        Перевірка створення замітки.
        """
        url = reverse('create_note')
        data = {
            'title': 'Test Note',
            'content': 'This is a test note.',
            'tags': [self.tag.id],
            'author': self.user.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Note.objects.count(), 1)
        self.assertEqual(Note.objects.get().title, 'Test Note')

    def test_delete_note(self):
        """
        Перевірка видалення замітки.
        """
        note = Note.objects.create(
            title='Test Note',
            content='Content of the test note',
            author=self.user
        )
        url = reverse('delete_note', kwargs={'pk': note.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Note.objects.count(), 0)