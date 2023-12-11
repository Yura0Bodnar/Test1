from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, generics, permissions
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import *
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.exceptions import PermissionDenied, NotFound


@method_decorator(csrf_exempt, name='dispatch')
class CreateUserView(APIView):

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateTagView(generics.CreateAPIView):
    serializer_class = TagSerializer

    def post(self, request, **kwargs):
        return self.create(request,  **kwargs)


class NoteCreateView(APIView):

    @swagger_auto_schema(
        request_body=NoteCreateSerializer,
        response={status.HTTP_201_CREATED: NoteCreateSerializer}
    )
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


class UserDeleteView(APIView):

    def delete(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({"message": "Invalid user_id."}, status=status.HTTP_404_NOT_FOUND)

        user.delete()
        return Response({"message": "Successful delete!"}, status=status.HTTP_204_NO_CONTENT)


class NoteUpdateView(APIView):

    @swagger_auto_schema(
        request_body=NoteSerializer(partial=True),
        responses={
            status.HTTP_200_OK: NoteSerializer(),
            status.HTTP_400_BAD_REQUEST: 'Bad Request',
            status.HTTP_404_NOT_FOUND: 'Not Found',
            status.HTTP_403_FORBIDDEN: 'Forbidden'
        }
    )
    def patch(self, request, user_id, note_id):
        note = self.get_object(note_id)
        self.check_editor_permission(user_id, note)

        serializer = NoteSerializer(note, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            Edit.objects.create(note=note, editor_id=user_id)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_object(self, note_id):
        try:
            return Note.objects.get(pk=note_id)
        except Note.DoesNotExist:
            raise NotFound({"message": "Not found note."})

    def check_editor_permission(self, user_id, note):
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            raise NotFound({"message": "User not found."})

        if user not in note.editors.all():
            raise PermissionDenied({"message": "You do not have permission to edit this note."})


class NoteSearchUserView(APIView):

    def get(self, request, author_id):
        try:
            user = User.objects.get(pk=author_id)
        except User.DoesNotExist:
            raise NotFound(detail="User not found.", code=status.HTTP_404_NOT_FOUND)

        notes = Note.objects.filter(author=user)
        serializer = NoteSerializer(notes, many=True)
        return Response(serializer.data)


class NoteSearchTagView(APIView):

    def get(self, request, tag_id):
        try:
            tag = Tag.objects.get(pk=tag_id)
        except Tag.DoesNotExist:
            raise NotFound(detail="Tag not found.", code=status.HTTP_404_NOT_FOUND)

        notes = Note.objects.filter(tags=tag)
        serializer = NoteSerializer(notes, many=True)
        return Response(serializer.data)


class StatisticView(APIView):

    def get(self, request):
        edit = Edit.objects.all()
        serializer = EditSerializer(edit, many=True)
        return Response(serializer.data)


class UserEditView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class TagEditView(generics.RetrieveUpdateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    def put(self, request, *args, **kwargs):
        """Update a tag."""
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        """Partially update a tag."""
        return self.partial_update(request, *args, **kwargs)