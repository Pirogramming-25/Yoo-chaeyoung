from django.urls import path
from . import views

app_name = "devtools"

urlpatterns = [
    path("", views.devtool_list, name="devtool-list"),
    path("create/", views.devtool_create, name="devtool-create"),
    path("<int:pk>/", views.devtool_detail, name="devtool-detail"),
    path("<int:pk>/update/", views.devtool_update, name="devtool-update"),
]
