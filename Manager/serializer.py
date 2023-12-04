from rest_framework import serializers
from .models import *
from django.core.exceptions import ValidationError


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class NoteCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Note
        fields = ['title', 'content', 'tags', 'author', 'editors']

    def validate(self, args):
        editors_data = args.get('editors', [])
        if len(editors_data) > 5:
            raise ValidationError('You cannot assign more than 5 editors.')
        return args

    def create(self, validated_data):
        tags_data = validated_data.pop('tags', None)
        editors_data = validated_data.pop('editors', None)

        note = Note.objects.create(**validated_data)

        if tags_data is not None:
            note.tags.set(tags_data)
        if editors_data is not None:
            note.editors.set(editors_data)

        return note


class NoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Note
        fields = "__all__"


class EditSerializer(serializers.ModelSerializer):

    class Meta:
        model = Edit
        fields = "__all__"

