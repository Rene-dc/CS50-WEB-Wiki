from django.urls import path

from . import views

app_name = "encyclopedia"

urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path("newpage", views.newpage, name="newpage"),
    path("select", views.editpageselect, name="editpageselect"),
    path("editpage/<str:entry>", views.editpage, name="editpage"),
    path("randompage", views.randompage, name="randompage"),
    path("wiki/<str:entry>", views.entrypage, name="entry")
]
