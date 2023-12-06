from django.contrib import admin
from django.urls import path
from .views import *


class CustomAdminSite(admin.AdminSite):
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('user/create/', self.admin_view(CreateUserView.as_view()), name='user-create'),
            path('user/<int:pk>/delete/', self.admin_view(UserDeleteView.as_view()), name='user-delete'),
            path('user/<int:pk>/edit/', self.admin_view(UserEditView.as_view()), name='user-edit'),

            path('tag/create/', self.admin_view(CreateTagView.as_view()), name='tag-create'),
            path('tag/<int:pk>/delete/', self.admin_view(TagDeleteView.as_view()), name='tag-delete'),
            path('tag/<int:pk>/edit/', self.admin_view(TagEditView.as_view()), name='tag-edit'),

            path('note/create/', self.admin_view(NoteCreateView.as_view()), name='note-create'),
            path('note/<int:pk>/delete/', self.admin_view(NoteDeleteView.as_view()), name='note-delete'),
            path('note/edit/<int:user_id>/<int:note_id>/', self.admin_view(NoteUpdateView.as_view()), name='note-edit'),

            path('note/search/user/<int:author_id>/', self.admin_view(NoteSearchUserView.as_view()), name='note-search-user'),
            path('note/search/tag/<int:tag_id>/', self.admin_view(NoteSearchTagView.as_view()), name='note-search-tag'),

            path('statistic/', self.admin_view(StatisticView.as_view()), name='statistic'),
        ]
        return custom_urls + urls


admin_site = CustomAdminSite(name='custom_admin')
