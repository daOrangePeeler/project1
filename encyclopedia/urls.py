from django.urls import path

from . import views

app_name = "encyclopedia"

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry_name>/", views.display_entry, name="display_entry"),
    path("new_entry/", views.new_entry, name="new_entry"),
    path("search/", views.search, name="search"),
    path("random_page/", views.random_page, name="random_page"),
    path("wiki/<str:entry_name>/edit/", views.edit_entry, name="edit_entry"),
]
