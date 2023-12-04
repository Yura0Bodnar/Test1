from django.urls import path
from .views import *

urlpatterns = [

    path('user/delete/<int:pk>/', UserDeleteView.as_view(), name='user_delete'),
    path('tag/delete/<int:pk>/', TagDeleteView.as_view(), name='tag_delete'),

    path('user/create/', CreateUserView.as_view(), name='create_user'),
    path('tag/create/', CreateTagView.as_view(), name='create_tag'),
    path('note/create/', NoteCreateView.as_view(), name='create_note'),
    path('note/delete/<int:pk>/', NoteDeleteView.as_view(), name='delete_note'),
    path('note/edit/<int:user_id>/<int:note_id>/', NoteUpdateView.as_view(), name='note_update'),
    path('note/search_by_user/<int:author_id>/', NoteSearchUserView.as_view(), name='note_search_user'),
    path('note/search_by_tag/<int:tag_id>/', NoteSearchTagView.as_view(), name='note_search_tag'),
    path('edit/get/', EditView.as_view(), name='edit_view'),
]
