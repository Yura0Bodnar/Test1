from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import *
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.exceptions import PermissionDenied, NotFound
from django.contrib.admin.views.decorators import staff_member_required


@method_decorator(csrf_exempt, name='dispatch')
class CreateUserView(APIView):

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateTagView(APIView):

    def post(self, request):
        serializer = TagSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NoteCreateView(APIView):

    def post(self, request):
        serializer = NoteCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NoteDeleteView(APIView):

    def delete(self, request, pk):
        try:
            note = Note.objects.get(pk=pk)
        except Note.DoesNotExist:
            return Response({"message": "Invalid note_id."}, status=status.HTTP_404_NOT_FOUND)

        note.delete()
        return Response({"message": "Successful delete!"}, status=status.HTTP_204_NO_CONTENT)


class TagDeleteView(APIView):

    def delete(self, request, pk):
        try:
            tag = Tag.objects.get(pk=pk)
        except Tag.DoesNotExist:
            return Response({"message": "Invalid tag_id."}, status=status.HTTP_404_NOT_FOUND)

        tag.delete()
        return Response({"message": "Successful delete!"}, status=status.HTTP_204_NO_CONTENT)


@method_decorator(staff_member_required, name='dispatch')
class UserDeleteView(APIView):

    def delete(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({"message": "Invalid user_id."}, status=status.HTTP_404_NOT_FOUND)

        user.delete()
        return Response({"message": "Successful delete!"}, status=status.HTTP_204_NO_CONTENT)


class NoteUpdateView(APIView):

    def patch(self, request, user_id, note_id):
        note = self.get_object(note_id)
        self.check_editor_permission(user_id, note)

        serializer = NoteSerializer(note, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            Edit.objects.create(note=note, editor_id=user_id)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_object(self, note_id):
        try:
            return Note.objects.get(pk=note_id)
        except Note.DoesNotExist:
            raise NotFound({"message": "Not found note."})  # Замініть Response на виключення NotFound

    def check_editor_permission(self, user_id, note):
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            raise NotFound({"message": "User not found."})  # Додайте обробку для випадку, коли користувач не знайдений

        if user not in note.editors.all():
            raise PermissionDenied({"message": "You do not have permission to edit this note."})


class NoteSearchUserView(APIView):

    def get(self, request, author_id):
        note = Note.objects.filter(author_id=author_id)
        serializer = NoteSerializer(note, many=True)
        return Response(serializer.data)


class NoteSearchTagView(APIView):

    def get(self, request, tag_id):
        note = Note.objects.filter(tags=tag_id)
        serializer = NoteSerializer(note, many=True)
        return Response(serializer.data)


class EditView(APIView):

    def get(self, request):
        edit = Edit.objects.all()
        serializer = EditSerializer(edit, many=True)
        return Response(serializer.data)
