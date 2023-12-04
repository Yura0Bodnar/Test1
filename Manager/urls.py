from django.urls import path
from .views import *

urlpatterns = [
    # path('user/create/', CreateUserView.as_view(), name='create_user'),
    # path('user/delete/<int:pk>/', UserDeleteView.as_view(), name='delete_note'),

    # path('tag/create/', CreateTagView.as_view(), name='create_tag'),
    # path('tag/delete/<int:pk>/', TagDeleteView.as_view(), name='delete_note'),

    # path('note/create/', NoteCreateView.as_view(), name='create_note'),
    # path('note/delete/<int:pk>/', NoteDeleteView.as_view(), name='delete_note'),
    # path('note/edit/<int:user_id>/<int:note_id>/', NoteUpdateView.as_view(), name='note-update'),
    # path('note/search_by_user/<int:author_id>/', NoteSearchUserView.as_view(), name='get_note_by_user'),
    # path('note/search_by_tag/<int:tag_id>/', NoteSearchTagView.as_view(), name='get_note_by_tag'),

    # path('edit/get/', EditView.as_view(), name='get_note_by_tag'),

    path('create_user/', CreateUserView.as_view(), name='create_user'),
    path('create_tag/', CreateTagView.as_view(), name='create_tag'),
    path('note_create/', NoteCreateView.as_view(), name='create_note'),
    path('note_delete/<int:pk>/', NoteDeleteView.as_view(), name='delete_note'),

]
