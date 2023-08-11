from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path("", views.index, name="index"),
    path("zone/login/", view=views.login_view, name="login"),
    path("zone/register/", view=views.register, name="register"),
    path("zone/site-send-zone", login_required(views.zonemain), name="zone"),
    path("zone/logout", view=views.logout_user, name="logout"),
    path("zone/zone/score-table", login_required(views.scoreTable), name="score_table"),
    path("zone/hacker-list/", login_required(views.hacker_list), name="hackers"),
    path("zone/search/search-user", login_required(views.search_user), name="search"),
    path(
        "zone/details/<str:id>/",
        (views.detailsPage),
        name="details",
    ),

]


handler404 = "pages.exceptions.handler404"
