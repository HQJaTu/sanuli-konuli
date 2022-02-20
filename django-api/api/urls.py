from django.urls import path, re_path
from . import views

urlpatterns = [
    path("heartbeat", views.heartbeat.API.as_view(), name="heartbeat"),
    re_path(
        r"^v(?P<version>(1))/words/(?P<lang>[^/]*)-(?P<word_length>[5-9])$",
        views.words.API.as_view(),
        name="words",
    ),
]
