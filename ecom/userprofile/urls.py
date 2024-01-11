from django.urls import path
from . import views

urlpatterns = [
    path("<int:pk>", views.profile, name="profile"),
    path("edit/<username>/", views.profile_edit, name="profile_edit"),
    path("onbroding", views.profile_edit, name="profile_onboarding"),
    path("followers/<int:pk>", views.followers, name="followers"),
    path("follows/<int:pk>", views.follows, name="follows"),
    path("unfollow/<int:pk>", views.unfollow, name="unfollow"),
    path("follow/<int:pk>", views.follow, name="follow"),
    path("inbox/", views.inbox, name="inbox"),
    path("conversation/<int:profile_id>/", views.conversation, name="conversation"),
    path("send_message/<int:profile_id>/", views.send_message, name="send_message"),
]
