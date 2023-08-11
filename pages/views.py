from django.contrib.auth import login, logout, authenticate
from django.core.paginator import Paginator
from django.shortcuts import  render, redirect
from django.contrib.auth.models import User
from django.db.models import F
from django.contrib import messages
from .forms import *
from .functions import *
from .models import Content, UserProfile, Domain, RankColor
from django.utils.html import escape
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods
from django.db import models
from django.db.models import Case, When, Value
from urllib.parse import unquote
from django.views.decorators.clickjacking import xframe_options_exempt
from .zonecontent import getPageContent


LEVEL_CHOICES_DICT = dict(UserProfile.LEVEL_CHOICES)
RANK_COLORS = {obj.rank: obj.color for obj in RankColor.objects.all()}


@require_http_methods(["GET"])
def index(request):
    totalUser = User.objects.count()
    totalZone = Content.objects.count()
    lastUser = Content.objects.last().user
    leader = (
        UserProfile.objects.select_related("user")
        .order_by("-total_points")
        .annotate(
            username=F("user__username"),
        )
        .values(
            "username",
        )
    ).first()
    results = (
        Content.objects.select_related(
            "user__userprofile",
            "domain",
        )
        .annotate(
            username=F("user__username"),
            status=F("user__userprofile__status"),
            rank=F("user__userprofile__rank"),
            domain_name=F("domain__domain_name"),
            site_urls=F("site_url"),
            domainstatus=F("domain__domainIsSpecial"),
            domain_ip=F("domain__ip_address"),
            id_=F("id"),
            country=F("domain__domainCountryCode"),
            date=F("domain__domainAddedDate"),
            site=F("site_url"),
        )
        .annotate(
            rank_name=Case(
                *[When(rank=k, then=Value(v)) for k, v in LEVEL_CHOICES_DICT.items()],
                output_field=models.CharField(),
            ),
            rank_color=Case(
                *[When(rank=k, then=Value(v)) for k, v in RANK_COLORS.items()],
                output_field=models.CharField(),
            ),
        )
        .values(
            "username",
            "status",
            "domain_name",
            "rank",
            "rank_name",
            "rank_color",
            "domainstatus",
            "domain_ip",
            "id_",
            "country",
            "date",
            "site",
        )
        .order_by("-id")
    )

    paginator = Paginator(results, 10)
    page_number = request.GET.get("page")
    ZONE = paginator.get_page(page_number)

    return render(
        request,
        "index.html",
        {
            "zone": ZONE,
            "totaluser": totalUser,
            "totalzone": totalZone,
            "lastzoneowner": lastUser,
            "leader": leader,
        },
    )


@csrf_protect
@require_http_methods(["GET", "POST"])
def login_view(request):
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        __username = escape(request.POST["username"])
        __password = escape(request.POST["password"])

        if form.is_valid():
            user = authenticate(request, username=__username, password=__password)
            if user is not None:
                login(request, user)
                return redirect("index")

            else:
                messages.error(
                    request,
                    "Invalid username or password.",
                )
                return redirect("login")
        else:
            messages.error(
                request,
                "Verification could not be completed, please try again.",
            )
            return redirect("login")

    else:
        form = UserLoginForm(request.POST)
        return render(request, "login.html", {"form": form})


@csrf_protect
@require_http_methods(["GET", "POST"])
def register(request):
    if request.method == "POST":
        __userForm = UserRegisterForm(request.POST)
        if __userForm.is_valid():
            __username = escape(__userForm.cleaned_data["username"])
            __password = escape(__userForm.cleaned_data["password"])
            __repassword = escape(__userForm.cleaned_data["repassword"])

            if (
                str(__password) == str(__repassword)
                and not User.objects.filter(username=__username).first()
                and passwordController(__password)
            ):
                User.objects.create_user(
                    username=__username, email=None, password=__password
                ).save()

                messages.success(
                    request,
                    "Account created successfully, please log in.",
                )
                return redirect("register")

            else:
                messages.error(
                    request,
                    "Error, please try again.",
                )
                return redirect("register")

        else:
            messages.error(
                request,
                "Verification could not be completed, please try again.",
            )
            return redirect("register")

    else:
        form = UserRegisterForm(request.POST)
        return render(request, "register.html", {"form": form})


@csrf_protect
@require_http_methods(["GET"])
def hacker_list(request):
    totalUser = User.objects.count()
    totalZone = Content.objects.count()
    lastUser = Content.objects.last().user
    leader = (
        UserProfile.objects.select_related("user")
        .order_by("-total_points")
        .annotate(
            username=F("user__username"),
        )
        .values(
            "username",
        )
    ).first()
    results = (
        UserProfile.objects.select_related("user")
        .order_by("-total_points")
        .annotate(
            username=F("user__username"),
            status_=F("user__userprofile__status"),
            ranks=F("user__userprofile__rank"),
            totalPoint=F("total_points"),
            joinDate=F("user__date_joined"),
            ids=F("id"),
        )
        .annotate(
            rank_name=Case(
                *[When(rank=k, then=Value(v)) for k, v in LEVEL_CHOICES_DICT.items()],
                output_field=models.CharField(),
            ),
            rank_color=Case(
                *[When(rank=k, then=Value(v)) for k, v in RANK_COLORS.items()],
                output_field=models.CharField(),
            ),
        )
        .values(
            "username",
            "status_",
            "ranks",
            "totalPoint",
            "joinDate",
            "rank_color",
            "rank_name",
            "ids",
        )
    )

    paginator = Paginator(results, 10)
    page_number = request.GET.get("page")
    ZONE = paginator.get_page(page_number)

    return render(
        request,
        "hackersList.html",
        {
            "users": ZONE,
            "totaluser": totalUser,
            "totalzone": totalZone,
            "lastzoneowner": lastUser,
            "leader": leader,
        },
    )


@csrf_protect
@require_http_methods(["GET", "POST"])
def zonemain(request):
    totalUser = User.objects.count()
    totalZone = Content.objects.count()
    lastUser = Content.objects.last().user
    leader = (
        UserProfile.objects.select_related("user")
        .order_by("-total_points")
        .annotate(
            username=F("user__username"),
        )
        .values(
            "username",
        )
    ).first()

    if request.method == "POST":
        url_ = ZoneUrlForm(request.POST)
        if url_.is_valid():
            urlAddress = escape(url_.cleaned_data["zone_main"]).split()
            for links in urlAddress:
                if str(links).startswith("http") or str(links).startswith("https"):
                    if not Content.objects.filter(site_url=links).exists():
                        try:
                            control = getDomainInformationsFromUrl(links)
                            content = getPageContent(links)
                        except requests.exceptions.ConnectionError as e:
                            continue

                        if control and content:
                            domain = Domain.objects.create(
                                domain_name=control["domain_name"],
                                extentions=control["extention"],
                                ip_address=control["ip_address"],
                                point=control["point"],
                                domainIsSpecial=control["is_special"],
                                domainCountryCode=control["country"],
                            )

                            Content.objects.create(
                                site_url=str(links),
                                user=request.user,
                                domain=domain,
                                content=content,
                            )
                            
                            

                        else:
                            messages.error(
                                request,
                                "The URL address is incorrect, please try again",
                            )
                            return redirect("zone")
                    else:
                        messages.error(
                            request,
                            "The URL address is already registered in the system, please try again",
                        )
                        return redirect("zone")
                else:
                    messages.error(
                        request, "The URL address is incorrect, please try again"
                    )
                    return redirect("zone")

            messages.success(request, "The URL addresses have been saved.")
            return redirect("zone")
        else:
            messages.error(request, "Verification failed, please try again")
            return redirect("zone")
    else:
        urlForm = ZoneUrlForm(request.POST)
        return render(
            request,
            "sendzone.html",
            {
                "form": urlForm,
                "totaluser": totalUser,
                "totalzone": totalZone,
                "lastzoneowner": lastUser,
                "leader": leader,
            },
        )


def scoreTable(request):
    leader = (
        UserProfile.objects.select_related("user")
        .order_by("-total_points")
        .annotate(
            username=F("user__username"),
        )
        .values(
            "username",
        )
    ).first()
    totalUser = User.objects.count()
    totalZone = Content.objects.count()
    lastUser = Content.objects.last().user

    totalList = (
        UserProfile.objects.select_related("user")
        .order_by("-total_points")
        .annotate(
            username=F("user__username"),
            status_=F("user__userprofile__status"),
            ranks=F("user__userprofile__rank"),
            totalPoint=F("total_points"),
            joinDate=F("user__date_joined"),
        )
        .annotate(
            rank_name=Case(
                *[When(rank=k, then=Value(v)) for k, v in LEVEL_CHOICES_DICT.items()],
                output_field=models.CharField(),
            ),
            rank_color=Case(
                *[When(rank=k, then=Value(v)) for k, v in RANK_COLORS.items()],
                output_field=models.CharField(),
            ),
        )
        .values(
            "username",
            "status_",
            "ranks",
            "totalPoint",
            "joinDate",
            "rank_color",
            "rank_name",
        )
    )
    paginator = Paginator(totalList, 10)
    page_number = request.GET.get("page")
    ZONE = paginator.get_page(page_number)

    return render(
        request,
        "scoretable.html",
        {
            "score": ZONE,
            "leader": leader,
            "totaluser": totalUser,
            "totalzone": totalZone,
            "lastzoneowner": lastUser,
        },
    )


##############################################


def logout_user(request):
    logout(request)
    return redirect("login")


@csrf_protect
@require_http_methods(["GET", "POST"])
def search_user(request):
    totalUser = User.objects.count()
    totalZone = Content.objects.count()
    lastUser = Content.objects.last().user
    leader = (
        UserProfile.objects.select_related("user")
        .order_by("-total_points")
        .annotate(
            username=F("user__username"),
        )
        .values(
            "username",
        )
    ).first()
    if request.method == "POST":
        form = SearchUserForm(request.POST)
        if form.is_valid():
            __username = escape(form.cleaned_data["search"])
            results = (
                Content.objects.select_related(
                    "user__userprofile",
                    "domain",
                )
                .annotate(
                    username=F("user__username"),
                    status=F("user__userprofile__status"),
                    rank=F("user__userprofile__rank"),
                    domain_name=F("domain__domain_name"),
                    site_urls=F("site_url"),
                    domainstatus=F("domain__domainIsSpecial"),
                    domain_ip=F("domain__ip_address"),
                    id_=F("id"),
                    country=F("domain__domainCountryCode"),
                    date=F("domain__domainAddedDate"),
                    site=F("site_url"),
                )
                .annotate(
                    rank_name=Case(
                        *[
                            When(rank=k, then=Value(v))
                            for k, v in LEVEL_CHOICES_DICT.items()
                        ],
                        output_field=models.CharField(),
                    ),
                    rank_color=Case(
                        *[When(rank=k, then=Value(v)) for k, v in RANK_COLORS.items()],
                        output_field=models.CharField(),
                    ),
                )
                .values(
                    "username",
                    "status",
                    "domain_name",
                    "rank",
                    "rank_name",
                    "rank_color",
                    "domainstatus",
                    "domain_ip",
                    "id_",
                    "country",
                    "date",
                    "site",
                )
                .order_by("-id")
                .filter(username__contains=__username)
            )
            paginator = Paginator(results, 3)
            page_number = request.GET.get("page")
            ZONE = paginator.get_page(page_number)

            if results:
                return render(
                    request,
                    "searchUser.html",
                    {
                        "form": form,
                        "zone": ZONE,
                        "status": True,
                        "totaluser": totalUser,
                        "totalzone": totalZone,
                        "lastzoneowner": lastUser,
                        "leader": leader,
                    },
                )
            else:
                messages.error(
                    request, message="I could not find any records for the user."
                )
                return redirect("search")

        else:
            ...
    else:
        form = SearchUserForm(request.POST)
        return render(
            request,
            "searchUser.html",
            {
                "form": form,
                "status": False,
                "totaluser": totalUser,
                "totalzone": totalZone,
                "lastzoneowner": lastUser,
                "leader": leader,
            },
        )


@csrf_protect
@require_http_methods(["GET"])
@xframe_options_exempt
def detailsPage(request, id):
    totalUser = User.objects.count()
    totalZone = Content.objects.count()
    lastUser = Content.objects.last().user
    leader = (
        UserProfile.objects.select_related("user")
        .order_by("-total_points")
        .annotate(
            username=F("user__username"),
        )
        .values(
            "username",
        )
    ).first()

    control = escape(id)
    control = unquote(control)
    try:
        results = (
            Content.objects.select_related(
                "user__userprofile",
                "domain",
            )
            .annotate(
                username=F("user__username"),
                status=F("user__userprofile__status"),
                rank=F("user__userprofile__rank"),
                domain_name=F("domain__domain_name"),
                site_urls=F("site_url"),
                domainstatus=F("domain__domainIsSpecial"),
                domain_ip=F("domain__ip_address"),
                id_=F("id"),
                country=F("domain__domainCountryCode"),
                date=F("domain__domainAddedDate"),
                site=F("site_url"),
                contents=F("content"),
            )
            .annotate(
                rank_name=Case(
                    *[
                        When(rank=k, then=Value(v))
                        for k, v in LEVEL_CHOICES_DICT.items()
                    ],
                    output_field=models.CharField(),
                ),
                rank_color=Case(
                    *[When(rank=k, then=Value(v)) for k, v in RANK_COLORS.items()],
                    output_field=models.CharField(),
                ),
            )
            .values(
                "username",
                "status",
                "domain_name",
                "rank",
                "rank_name",
                "rank_color",
                "domainstatus",
                "domain_ip",
                "id_",
                "country",
                "date",
                "site",
                "contents",
                "site_urls",
            )
            .order_by("-id")
            .filter(id=control)
        )
    except:
        return redirect("index")

    return render(
        request,
        "details.html",
        {
            "result": results,
            "totaluser": totalUser,
            "totalzone": totalZone,
            "lastzoneowner": lastUser,
            "leader": leader,
        },
    )
