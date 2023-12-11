from django.urls import path
from .views import *

urlpatterns = [

    path('user/create/', CreateUserView.as_view(), name='user-create'),
    path('user/<int:pk>/delete/', UserDeleteView.as_view(), name='user-delete'),
    path('user/<int:pk>/edit/', UserEditView.as_view(), name='user-edit'),

    path('tag/create/', CreateTagView.as_view(), name='tag-create'),
    path('tag/delete/<int:pk>/', TagDeleteView.as_view(), name='tag-delete'),
    path('tag/<int:pk>/edit/', TagEditView.as_view(), name='tag-edit'),

    path('note/create/', NoteCreateView.as_view(), name='note-create'),
    path('note/delete/<int:pk>/', NoteDeleteView.as_view(), name='note-delete'),
    path('note/edit/<int:user_id>/<int:note_id>/', NoteUpdateView.as_view(), name='note-update'),

    path('note/search_by_tag/<int:tag_id>/', NoteSearchTagView.as_view(), name='note-search-tag'),
    path('note/search/user/<int:author_id>/', NoteSearchUserView.as_view(), name='note-search-user'),
]

