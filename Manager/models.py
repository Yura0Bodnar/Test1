from django.db import models
from django.contrib.auth.models import User


class Tag(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        db_table = "Tag"


class Note(models.Model):
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=404)
    tags = models.ManyToManyField(Tag, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes')
    editors = models.ManyToManyField(User, blank=True, related_name='editable_notes')
    last_edited = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "Note"


class Edit(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='edits')
    editor = models.ForeignKey(User, on_delete=models.CASCADE)
    edit_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "Edit"

