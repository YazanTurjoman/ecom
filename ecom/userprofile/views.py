from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .form import ProfileForm
from django.urls import reverse
from django.http import Http404
from django.contrib.auth.models import User
from .models import Profile, Message, Notification
from django.db.models import Q  # Import the Q object
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


# views.py


@login_required
def inbox(request):
    user_profile = Profile.objects.get(user=request.user)

    all_messages = Message.objects.filter(
        Q(sender=user_profile) | Q(receiver=user_profile)
    ).order_by(
        "-timestamp"
    )  # Order by timestamp in descending order

    conversations = {}

    for message in all_messages:
        if message.sender == user_profile:
            other_profile = message.receiver
        else:
            other_profile = message.sender

        if other_profile not in conversations:
            conversations[other_profile] = message

    sorted_conversations = sorted(
        conversations.values(), key=lambda x: x.timestamp, reverse=True
    )

    return render(request, "inbox.html", {"conversations": sorted_conversations})


@login_required
def conversation(request, profile_id):
    user_profile = Profile.objects.get(user=request.user)
    other_profile = Profile.objects.get(id=profile_id)
    messages = Message.objects.filter(
        (Q(sender=user_profile) & Q(receiver=other_profile))
        | (Q(sender=other_profile) & Q(receiver=user_profile))
    ).order_by("timestamp")
    return render(
        request,
        "conversation.html",
        {"other_profile": other_profile, "messages": messages},
    )


@login_required
def send_message(request, profile_id):
    if request.method == "POST":
        content = request.POST["content"]
        sender = Profile.objects.get(user=request.user)
        receiver = Profile.objects.get(id=profile_id)

        Message.objects.create(sender=sender, receiver=receiver, content=content)

        # Notify the receiver
        Notification.objects.create(
            user=receiver, message=f"You have a new message from {sender.name}"
        )

        return redirect("conversation", profile_id=profile_id)
    else:
        # Handle other HTTP methods or render a form
        pass


def profile(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=pk)

        # Post Form logic
        if request.method == "POST":
            # Get current user
            current_user_profile = request.user.profile
            # Get form data
            action = request.POST["follow"]
            # Decide to follow or unfollow
            if action == "unfollow":
                current_user_profile.followers.remove(profile)
            elif action == "follow":
                current_user_profile.followers.add(profile)
            # Save the profile
            current_user_profile.save()

        return render(
            request,
            "profile.html",
            {
                "profile": profile,
            },
        )
    else:
        messages.success(request, ("You Must Be Logged In To View This Page..."))
        return redirect("home")


def profile_edit(request, username):
    user = get_object_or_404(User, username=username)
    form = ProfileForm(instance=request.user.profile)
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()

    if request.path == reverse("profile_onboarding"):
        template = "profile_onboarding.html"
    else:
        template = "editprofile.html"

        return render(request, template, {"form": form})


def followers(request, pk):
    if request.user.is_authenticated:
        if request.user.id == pk:
            profiles = Profile.objects.get(user_id=pk)
            return render(request, "followers.html", {"profiles": profiles})
        else:
            messages.success(request, ("That's Not Your Profile Page..."))
            return redirect("home")
    else:
        messages.success(request, ("You Must Be Logged In To View This Page..."))
        return redirect("home")


def follows(request, pk):
    if request.user.is_authenticated:
        if request.user.id == pk:
            profile = Profile.objects.get(user_id=pk)
            return render(request, "follows.html", {"profile": profile})
        else:
            messages.success(request, ("That's Not Your Profile Page..."))
            return redirect("home")
    else:
        messages.success(request, ("You Must Be Logged In To View This Page..."))
        return redirect("home")


def unfollow(request, pk):
    if request.user.is_authenticated:
        # Get the profile to unfollow
        profile = Profile.objects.get(user_id=pk)
        # Unfollow the user
        request.user.profile.followers.remove(profile)
        # Save our profile
        request.user.profile.save()

        # Return message
        messages.success(
            request, (f"You Have Successfully Unfollowed {profile.user.username}")
        )
        return redirect(request.META.get("HTTP_REFERER"))

    else:
        messages.success(request, ("You Must Be Logged In To View This Page..."))
        return redirect("home")


def follow(request, pk):
    if request.user.is_authenticated:
        # Get the profile to unfollow
        profile = Profile.objects.get(user_id=pk)
        # Unfollow the user
        request.user.profile.follows.add(profile)
        # Save our profile
        request.user.profile.save()

        # Return message
        messages.success(
            request, (f"You Have Successfully Followed {profile.user.username}")
        )
        return redirect(request.META.get("HTTP_REFERER"))

    else:
        messages.success(request, ("You Must Be Logged In To View This Page..."))
        return redirect("home")
