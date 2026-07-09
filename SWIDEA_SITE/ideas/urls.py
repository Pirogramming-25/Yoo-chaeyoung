from django.urls import path
from . import views

app_name = "ideas"

urlpatterns = [
    path("", views.idea_list, name="idea-list"),
    path("create/", views.idea_create, name="idea-create"),
    path("<int:pk>/", views.idea_detail, name="idea-detail"),
    path("<int:pk>/update/", views.idea_update, name="idea-update"),
    path("<int:pk>/delete/", views.idea_delete, name="idea-delete"),
]