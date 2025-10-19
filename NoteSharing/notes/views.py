from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import AddNoteForm, AddNoteTagsForm
from .models import Note, NoteTag


def _attach_new_tags(note: Note, raw_tags: str) -> None:
    """Attach any comma-separated tags from the raw string to the note."""
    if not raw_tags:
        return

    seen = set()
    for raw in raw_tags.split(","):
        title = raw.strip()
        if not title or title in seen:
            continue
        seen.add(title)
        tag, _ = NoteTag.objects.get_or_create(title=title)
        note.tags.add(tag)


@login_required
def addNote(request):
    if request.method == "POST":
        note_form = AddNoteForm(request.POST, request.FILES)
        if note_form.is_valid():
            note = note_form.save(commit=False)
            note.author = request.user.profile
            note.save()

            _attach_new_tags(note, note_form.cleaned_data.get("new_tags", ""))

            messages.success(request, "Note created successfully.")
            return redirect("dashboard")
    else:
        note_form = AddNoteForm()

    context = {
        "note_form": note_form,
    }
    return render(request, "addNote.html", context=context)


def viewNote(request, pk):
    note = get_object_or_404(Note, pk=pk)
    author_profile = note.author
    viewer_profile = request.user.profile if request.user.is_authenticated else None

    profile_url = "#"
    if author_profile and getattr(author_profile, "user", None):
        if request.user.is_authenticated and request.user == author_profile.user:
            profile_url = reverse("dashboard")

    context = {
        "profile": author_profile,
        "note": note,
        "viewer_profile": viewer_profile,
        "viewer": request.user if request.user.is_authenticated else None,
        "profile_url": profile_url,
    }
    return render(request, "viewNote.html", context=context)


@login_required
def editNote(request, pk):
    note = get_object_or_404(Note, pk=pk, author=request.user.profile)

    if request.method == "POST":
        intent = request.POST.get("intent")

        if intent == "attach-tag":
            note_form = AddNoteForm(instance=note)
            note_form.initial["new_tags"] = ""

            tag_form = AddNoteTagsForm(request.POST)
            if tag_form.is_valid():
                title = tag_form.cleaned_data["title"].strip()
                if title:
                    tag, _ = NoteTag.objects.get_or_create(title=title)
                    note.tags.add(tag)
                    messages.success(request, f'Tag "{title}" attached to the note.')
                    return redirect("editNote", pk=note.pk)

                tag_form.add_error("title", "Please enter a valid tag title.")
        else:
            note_form = AddNoteForm(request.POST, request.FILES, instance=note)
            tag_form = AddNoteTagsForm()
            if note_form.is_valid():
                updated_note = note_form.save()
                _attach_new_tags(updated_note, note_form.cleaned_data.get("new_tags", ""))
                messages.success(request, "Note updated successfully.")
                return redirect("viewNote", pk=note.pk)
    else:
        note_form = AddNoteForm(instance=note)
        note_form.initial["new_tags"] = ""
        tag_form = AddNoteTagsForm()

    context = {
        "note": note,
        "note_form": note_form,
        "tag_form": tag_form,
    }
    return render(request, "editNote.html", context=context)
