from django.urls import path
from .views import viewNote,editNote,addNote
urlpatterns = [
    path('addNote/',addNote,name="addNote"),
    path('viewNote/<int:pk>',viewNote,name="viewNote"),
    path('notes/<int:pk>/edit/',editNote, name="editNote"),
]