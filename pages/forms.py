from django import forms

from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox


class UserLoginForm(forms.Form):
    username = forms.CharField(
        label="Username",
        max_length=20,
        min_length=3,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control  border-3",
                "name": "username",
                "id": "inputEmailAddress",
                "placeholder": "Enter username",
            }
        ),
    )

    password = forms.CharField(
        label="Password",
        min_length=5,
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control border-end-0  border-3",
                "name": "password",
                "id": "inputChoosePassword",
                "placeholder": "Enter password",
            }
        ),
    )

    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())

    def clean(self):
        cleaned_data = super().clean()
        captcha_value = cleaned_data.get("captcha")
        if not captcha_value:
            raise forms.ValidationError("Captcha doğrulama hatası")
        return cleaned_data


class UserRegisterForm(forms.Form):
    username = forms.CharField(
        label="Username",
        max_length=20,
        min_length=3,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control  border-3",
                "name": "username",
                "id": "inputEmailAddress",
                "placeholder": "Enter username",
            }
        ),
    )

    password = forms.CharField(
        label="Password",
        min_length=5,
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control border-end-0  border-3",
                "name": "password",
                "id": "inputChoosePassword",
                "placeholder": "Enter password",
            }
        ),
    )

    repassword = forms.CharField(
        label="Re-Password",
        min_length=5,
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control border-end-0  border-3",
                "name": "repassword",
                "id": "inputChoosePassword",
                "placeholder": "Enter re-password",
            }
        ),
    )

    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())

    def clean(self):
        cleaned_data = super().clean()
        captcha_value = cleaned_data.get("captcha")
        if not captcha_value:
            raise forms.ValidationError("Captcha doğrulama hatası")
        return cleaned_data


class ZoneUrlForm(forms.Form):
    zone_main = forms.CharField(
        label="Web site url",
        min_length=5,
        required=True,
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "name": "zone_class",
                "placeholder": "Enter web url",
                "cols": 100,
                "rows": 10,
                "style": "resize:none;",
            }
        ),
    )

    def clean_links(self):
        links = self.changed_data["zone_main"]
        linksList = links.split()
        validateUrl = URLValidator()

        for link in linksList:
            try:
                validateUrl(link)
            except ValidationError:
                raise forms.ValidationError(f"{link} Geçersiz")

        return links

    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())

    def clean(self):
        cleaned_data = super().clean()
        captcha_value = cleaned_data.get("captcha")
        if not captcha_value:
            raise forms.ValidationError("Captcha doğrulama hatası")
        return cleaned_data


class SearchUserForm(forms.Form):
    search = forms.CharField(
        label="Search User ",
        min_length=1,
        max_length=20,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "name": "searchForm",
                "placeholder": "Enter username ",
            }
        ),
    )

    """captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())

    def clean(self):
        cleaned_data = super().clean()
        captcha_value = cleaned_data.get("captcha")
        if not captcha_value:
            raise forms.ValidationError("Captcha doğrulama hatası")
        return cleaned_data"""
