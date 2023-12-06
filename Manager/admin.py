from django.contrib import admin
from django.urls import path
from .views import *


class CustomAdminSite(admin.AdminSite):
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('create_user/', self.admin_view(CreateUserView.as_view()), name='create_user'),
            path('create_tag/', self.admin_view(CreateTagView.as_view()), name='create_tag'),
            path('create_note/', self.admin_view(NoteCreateView.as_view()), name='create_note'),
            path('note/<int:pk>/delete/', self.admin_view(NoteDeleteView.as_view()), name='note_delete'),
            path('tag/<int:pk>/delete/', self.admin_view(TagDeleteView.as_view()), name='tag_delete'),
            path('user/<int:pk>/delete/', self.admin_view(UserDeleteView.as_view()), name='user_delete'),
            path('note/<int:user_id>/<int:note_id>/update/', self.admin_view(NoteUpdateView.as_view()), name='note_update'),
            path('note/search/user/<int:author_id>/', self.admin_view(NoteSearchUserView.as_view()), name='note_search_user'),
            path('note/search/tag/<int:tag_id>/', self.admin_view(NoteSearchTagView.as_view()), name='note_search_tag'),
            path('edits/', self.admin_view(EditView.as_view()), name='edit_list'),
        ]
        return custom_urls + urls


admin_site = CustomAdminSite(name='custom_admin')
