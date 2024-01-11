from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about", views.about, name="about"),
    path("login/", views.login_user, name="login"),
    path("logout", views.logout_user, name="logout"),
    path("register", views.register_user, name="register"),
    path("product/<int:pk>", views.product, name="product"),
    path("category/<str:foo>", views.category, name="category"),
    path("category_summary/", views.category_summary, name="category_summary"),
    path("like/<pk>/", views.like_product, name="like_product"),
    path("movies/add/", views.add_movie, name="add_movie"),
    path("movies/<int:pk>/update/", views.update_movie, name="update_movie"),
    path("movies/<int:pk>/delete/", views.delete_movie, name="delete_movie"),
    # path("actors/", views.ActorListView.as_view(), name="actor_list"),
    # path("actors/<int:pk>/", views.ActorDetailView.as_view(), name="actor_detail"),
    path("actors/", views.all_actors, name="all_actors"),
    path("actors/add/", views.add_actor, name="add_actor"),
    path("actors/<int:pk>/update/", views.update_actor, name="update_actor"),
    path("actors/<int:pk>/delete/", views.delete_actor, name="delete_actor"),
]
