from bma_app.forms import CreateNoteForm
from bma_app.views.api import ApiViewSet
from bma_app.views.serializers import ApiSerializer
from common.models.generic import generic_fk
from django.http import HttpResponse, JsonResponse
from main.models import Note, RelatedFile
from main.util import get_media_type_description
from main.views.querysets import get_notes
from rest_framework import serializers
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.request import Request


class MediaSerializer(ApiSerializer):
    file = serializers.FileField(write_only=True)
    type = serializers.SerializerMethodField(read_only=True)

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
    content = serializers.CharField(write_only=True)
    content_html = serializers.CharField(read_only=True)
    timestamp = serializers.DateTimeField(source="created_at", read_only=True)
    url = serializers.URLField(source="get_absolute_url", read_only=True)
    media = MediaSerializer(source="related_files", many=True)

    class Meta:
        model = Note
        fields = [
            "id",
            "content",
            "content_html",
            "url",
            "timestamp",
            "is_published",
            "media",
        ]


class NotesViewSet(ApiViewSet):
    queryset = get_notes()
    parser_classes = [FormParser, MultiPartParser]
    serializer_class = NotesSerializer

    def create(self, request: Request, *args, **kwargs):
        form = CreateNoteForm(request.POST, request.FILES)
        if not form.is_valid():
            return HttpResponse(status=401)

        content = form.cleaned_data.get("content")
        note = Note.objects.create(content=content.strip())

        if form.files:
            RelatedFile.objects.create(
                file=form.files["file"],
                description=form.cleaned_data.get("file_description"),
                **generic_fk(note),
            )

        return JsonResponse({"id": note.api_id}, status=201)
