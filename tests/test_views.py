from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from Manager.models import *


class UserDeleteViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_delete_user(self):
        url = reverse('user-delete', kwargs={'pk': self.user.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_user_invalid_id(self):
        url = reverse('user-delete', kwargs={'pk': 0})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class UserEditViewTest(APITestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        # URL for updating user
        self.update_url = reverse('user-edit', kwargs={'pk': self.user.pk})

    def test_update_user_put(self):
        # Data for updating user
        data = {'username': 'newusername', 'password': 'newpassword123'}

        response = self.client.put(self.update_url, data)

        # Check if the update was successful
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, data['username'])

    def test_update_user_patch(self):
        # Data for partial update
        data = {'username': 'patchedusername'}

        response = self.client.patch(self.update_url, data)

        # Check if the partial update was successful
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, data['username'])

    def tearDown(self):
        self.user.delete()


class TagCreateTests(APITestCase):

    def test_create_tag(self):
        """
        Перевірка створення тегу.
        """
        url = reverse('tag-create')
        data = {'name': 'Personal'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class TagDeleteViewTests(APITestCase):
    def setUp(self):
        self.tag = Tag.objects.create(name='Test Tag')

    def test_delete_tag(self):
        url = reverse('tag-delete', kwargs={'pk': self.tag.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_tag_invalid_id(self):
        url = reverse('tag-delete', kwargs={'pk': 999})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class NoteCreateTests(APITestCase):

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
        url = reverse('note-create')
        data = {
            'title': 'Test Note',
            'content': 'This is a test note.',
            'tags': [self.tag.id],
            'author': self.user.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete_note(self):
        """
        Перевірка видалення замітки.
        """
        note = Note.objects.create(
            title='Test Note',
            content='Content of the test note',
            author=self.user
        )
        url = reverse('note-delete', kwargs={'pk': note.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class NoteUpdateViewTests(APITestCase):
    def setUp(self):
        # Створіть тестових користувачів
        self.user1 = User.objects.create_user(username='user1', password='testpass1')
        self.user2 = User.objects.create_user(username='user2', password='testpass2')

        # Створіть теги для тестової замітки
        self.tag1 = Tag.objects.create(name='tag1')

        # Створіть замітку, яку буде редагувати користувач
        self.note = Note.objects.create(
            title='Initial Title',
            content='Initial content.',
            author=self.user1
        )
        self.note.editors.add(self.user1)

        # URL для редагування замітки
        self.url = reverse('note-update', kwargs={'user_id': self.user1.id, 'note_id': self.note.id})

        # Дані для оновлення замітки
        self.data = {'title': 'Updated Title', 'content': 'Updated content.', 'tags': [self.tag1.id]}

    def test_update_note_permission(self):
        # Використовуйте self.client.patch для відправки запиту на оновлення
        self.client.force_authenticate(user=self.user1)  # Аутентифікуйте користувача, який має дозвіл на редагування
        response = self.client.patch(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Перевірте, чи дані замітки оновлені
        self.note.refresh_from_db()
        self.assertEqual(self.note.title, 'Updated Title')
        self.assertEqual(self.note.content, 'Updated content.')
        self.assertTrue(self.tag1 in self.note.tags.all())


class NoteSearchTagViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user', password='testpass')
        self.tag = Tag.objects.create(name='tag')
        self.note = Note.objects.create(title='Note', content='Content', author=self.user)
        self.note.tags.add(self.tag)

    def test_search_notes_by_tag(self):
        url = reverse('note-search-tag', kwargs={'tag_id': self.tag.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_search_notes_by_invalid_tag_id(self):
        # Use an invalid tag ID, such as 0, which should not exist.
        url = reverse('note-search-tag', kwargs={'tag_id': 0})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class NoteSearchUserViewTest(APITestCase):
    def setUp(self):
        # Create users
        self.user1 = User.objects.create_user(username='user1', password='12345')
        self.user2 = User.objects.create_user(username='user2', password='12345')

        # Create notes for user1
        Note.objects.create(title='Note 1', content='Content 1', author=self.user1)
        Note.objects.create(title='Note 2', content='Content 2', author=self.user1)

        # Create a note for user2
        Note.objects.create(title='Note 3', content='Content 3', author=self.user2)

    def test_get_notes_for_user(self):
        # URL for getting notes of user1
        url = reverse('note-search-user', kwargs={'author_id': self.user1.pk})

        response = self.client.get(url)

        # Check if the response is correct
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # 2 notes for user1

        # Validate the data (optional, based on what you include in your serializer)
        for note_data in response.data:
            self.assertEqual(note_data['author'], self.user1.pk)

    def test_user_not_found(self):
        # URL for a non-existent user
        url = reverse('note-search-user', kwargs={'author_id': 999})

        response = self.client.get(url)

        # Check if the response is 404 Not Found
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def tearDown(self):
        # Clean up any objects created
        Note.objects.all().delete()
        User.objects.all().delete()
