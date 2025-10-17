from django.urls import path
from .views import addNote
urlpatterns = [
    path('addNote/',addNote,name="addNote"),
    # path('editNote/',editNote,name="editNote"),
]