from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import AddNoteForm
from .models import NoteTag


@login_required
def addNote(request):
    if request.method == "POST":
        note_form = AddNoteForm(request.POST, request.FILES)
        if note_form.is_valid():
            note = note_form.save(commit=False)
            note.author = request.user.profile
            note.save()

            new_tags = note_form.cleaned_data.get("new_tags", "")
            if new_tags:
                raw_tags = new_tags.split(",")
                tag_titles = []
                for tag in raw_tags:
                    cleaned_tag = tag.strip()
                    if cleaned_tag:
                        tag_titles.append(cleaned_tag)

                for title in tag_titles:
                    tag, _ = NoteTag.objects.get_or_create(title=title)
                    note.tags.add(tag)

            messages.success(request, "Note created successfully.")
            return redirect("dashboard")
    else:
        note_form = AddNoteForm()

    context = {
        "note_form": note_form,
    }
    return render(request, "addNote.html", context=context)
