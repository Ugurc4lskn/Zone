from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.core.validators import RegexValidator

import re
from django.db.models import Sum


class UserProfile(models.Model):
    LEVEL_CHOICES = [
        (1, "Junior"),
        (2, "Senior"),
        (3, "Expert"),
        (4, "Supreme"),
        (5, "Defacer"),
        (6, "Hacker"),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    rank = models.IntegerField(choices=LEVEL_CHOICES, default=1)
    total_points = models.IntegerField(default=0)
    

    def update_rank(self):
        total_points = Content.objects.filter(user=self.user).aggregate(
            Sum("domain__point")
        )["domain__point__sum"]

        if total_points:
            self.total_points = total_points
            self.save()

        if total_points is None:
            total_points = 0

        if total_points < 100:
            self.rank = 1

        elif total_points <= 220:
            self.rank = 2

        elif total_points < 350:
            self.rank = 3

        elif total_points < 600:
            self.rank = 4

        elif total_points < 900:
            self.rank = 5
        else:
            self.rank = 6

        self.save()

    def __str__(self):
        return self.user.username


class RankColor(models.Model):
    rank = models.IntegerField(choices=UserProfile.LEVEL_CHOICES)
    color = models.CharField(max_length=50, default="")
    color_id = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.get_rank_display()} - {self.color}"


class Domain(models.Model):
    domain_name = models.CharField(max_length=50)
    extentions = models.CharField(max_length=50)
    ip_address = models.CharField(
        max_length=50,
        validators=[
            RegexValidator(
                re.compile("^([0-9]{1,3}\.){3}[0-9]{1,3}$"), "Invalid IP Address"
            )
        ],
    )
    point = models.IntegerField()
    domainIsSpecial = models.BooleanField(default=False)
    domainCountryCode = models.CharField(max_length=30, default="")
    domainAddedDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.domain_name


class Content(models.Model):
    site_url = models.URLField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE)
    content = models.TextField()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        user_profile = UserProfile.objects.get(user=self.user)
        user_profile.update_rank()

    def __str__(self):
        return self.site_url
