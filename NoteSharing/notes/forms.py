from django import forms

from .models import Note, NoteTag


class AddNoteForm(forms.ModelForm):
    new_tags = forms.CharField(
        required=False,
        label="Tags",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Work, Personal, Ideas",
                "class": "w-full border-none bg-transparent text-[#3b2f2f] text-sm focus:outline-none focus:ring-0",
            }
        ),
    )

    class Meta:
        model = Note
        fields = ["title", "content", "image"]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "placeholder": "Enter a descriptive title",
                    "class": "w-full border-none bg-transparent text-[#3b2f2f] text-base focus:outline-none focus:ring-0",
                }
            ),
            "content": forms.Textarea(
                attrs={
                    "placeholder": "Write your note content here…",
                    "rows": 8,
                    "class": "w-full border-none bg-transparent text-[#3b2f2f] text-sm leading-relaxed focus:outline-none focus:ring-0",
                }
            ),
            "image": forms.ClearableFileInput(
                attrs={
                    "class": "block w-full text-sm text-[#3b2f2f] file:mr-4 file:rounded-full file:border-0 file:bg-[#f0ded0] file:px-4 file:py-2 file:text-sm file:font-semibold file:text-[#3b2f2f] hover:file:bg-[#e2c7b0]",
                }
            ),
        }
        labels = {
            "title": "Title",
            "content": "Content",
            "image": "Attach an image",
        }

    field_order = ["title", "content", "image", "new_tags"]


class AddNoteTagsForm(forms.ModelForm):
    class Meta:
        model = NoteTag
        fields = ["title"]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "placeholder": "e.g. Work, Personal, Ideas",
                    "class": "w-full border-none bg-transparent text-[#3b2f2f] text-sm focus:outline-none focus:ring-0",
                }
            )
        }
        labels = {
            "title": "Tag title",
        }
