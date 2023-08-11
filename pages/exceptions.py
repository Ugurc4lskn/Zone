from django.shortcuts import render, redirect


def handler404(request, *args, **argv):
    response = render(request, "404.html")
    response.status_code = 404
    return response
