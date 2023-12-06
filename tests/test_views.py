from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from Manager.models import *
from Manager.serializer import EditSerializer


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
        self.url = reverse('note_update', kwargs={'user_id': self.user1.id, 'note_id': self.note.id})

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


class EditViewTests(APITestCase):
    def setUp(self):
        # Створіть тестових користувачів
        self.user = User.objects.create_user(username='testuser', password='testpass')

        # Створіть тестові замітки
        self.note = Note.objects.create(
            title='Test Note',
            content='Test content',
            author=self.user
        )

        # Створіть тестові записи редагування
        self.edit = Edit.objects.create(
            note=self.note,
            editor=self.user
        )

    def test_get_edits(self):
        """
        Перевірка отримання списку всіх записів редагування.
        """
        url = reverse('statistic')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Перевірка кількості записів редагування
        edits = Edit.objects.all()
        serializer = EditSerializer(edits, many=True)
        self.assertEqual(response.data, serializer.data)


class TagDeleteViewTests(APITestCase):
    def setUp(self):
        self.tag = Tag.objects.create(name='Test Tag')

    def test_delete_tag(self):
        url = reverse('tag-delete', kwargs={'pk': self.tag.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Tag.objects.count(), 0)

    def test_delete_tag_invalid_id(self):
        url = reverse('tag-delete', kwargs={'pk': 999})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class UserDeleteViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_delete_user(self):
        url = reverse('user-delete', kwargs={'pk': self.user.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.count(), 0)

    def test_delete_user_invalid_id(self):
        url = reverse('user-delete', kwargs={'pk': 0})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
