from bma_app.forms import AppendNoteMediaForm, CreateNoteForm, MediaAttachmentForm
from bma_app.views.api import ApiViewSet
from bma_app.views.serializers import ApiSerializer
from common.models.generic import generic_fk
from django.http import HttpResponse
from main.models import Note, RelatedFile
from main.util import get_media_type_description
from rest_framework import serializers, status
from rest_framework.decorators import action
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.request import Request
from rest_framework.response import Response


def bad_request():
    return HttpResponse(status=status.HTTP_400_BAD_REQUEST)


class MediaSerializer(ApiSerializer):
    file = serializers.FileField()
    type = serializers.SerializerMethodField()

    def get_type(self, file: RelatedFile):
        return get_media_type_description(file)

    class Meta:
        model = RelatedFile
        fields = [
            "id",
            "file",
            "url",
            "description",
            "type",
        ]


class NotesSerializer(ApiSerializer):
    id = serializers.CharField(read_only=True)
    content_html = serializers.CharField(read_only=True)
    content = serializers.CharField(write_only=True)
    timestamp = serializers.DateTimeField(source="created_at", read_only=True)
    url = serializers.URLField(source="get_absolute_url", read_only=True)
    media = MediaSerializer(source="related_files", many=True, read_only=True)

    class Meta:
        model = Note
        fields = [
            "id",
            "content_html",
            "content",
            "url",
            "timestamp",
            "is_published",
            "media",
        ]


class NotesViewSet(ApiViewSet):
    queryset = Note.objects.all()
    parser_classes = [FormParser, MultiPartParser, JSONParser]
    serializer_class = NotesSerializer
    lookup_field = "api_id"

    def create(self, request: Request, *args, **kwargs):
        form = CreateNoteForm(request.POST, request.FILES)
        if not form.is_valid():
            return bad_request()

        note = Note.objects.create(content=form.cleaned_data.get("content"))

        if form.files:
            _create_related_file(note, form)

        return Response({"id": note.api_id}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"])
    def media(self, request, *args, **kwargs):
        note = self.get_object()
        form = AppendNoteMediaForm(request.POST, request.FILES)

        if not form.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST)

        file = _create_related_file(note, form)
        return Response({"id": file.api_id}, status=status.HTTP_201_CREATED)


def _create_related_file(note: Note, form: MediaAttachmentForm):
    return RelatedFile.objects.create(
        file=form.files["file"],
        description=form.cleaned_data.get("file_description"),
        **generic_fk(note),
    )
