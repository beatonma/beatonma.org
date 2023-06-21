from bma_app.forms import CreateNoteForm, RelatedFileForm
from bma_app.views import AppApiView
from common.models.generic import generic_fk
from django.http import HttpRequest, HttpResponse, JsonResponse
from main.models import Note, RelatedFile


class CreateNoteView(AppApiView):
    def post(self, request: HttpRequest):
        form = CreateNoteForm(request.POST, request.FILES)
        if not form.is_valid():
            return HttpResponse(status=400)

        return _create_note(form, request)

    def delete(self, request: HttpRequest):
        return HttpResponse(status=403)


def _create_note(form: CreateNoteForm, request: HttpRequest) -> HttpResponse:
    content = form.cleaned_data.get("content")
    note = Note.objects.create(content=content.strip())

    _upload_file(note, RelatedFileForm(request.POST, request.FILES))

    return JsonResponse({"id": note.pk}, status=200)


def _upload_file(note: Note, form: RelatedFileForm):
    if form.is_valid():
        RelatedFile.objects.create(
            file=form.files["file"],
            description=form.cleaned_data.get("file_description"),
            **generic_fk(note),
        )
