from django.contrib import admin
from django.urls import path
from memos import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.memo_list, name="memo_list"),
    path("memos/new/", views.create_memo, name="create_memo"),
    path("memos/<int:memo_id>/", views.memo_detail, name="memo_detail"),
    path("memos/<int:memo_id>/edit/", views.edit_memo, name="edit_memo"),
    path("memos/<int:memo_id>/delete/", views.delete_memo, name="delete_memo"),
]
