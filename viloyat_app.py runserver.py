
"""
Bitta faylda to'liq Django ilovasi.
Ishlatish:
    pip install django
    python viloyat_app.py runserver
"""

import os
import sys
import django
from django.conf import settings
from django.urls import path
from django.http import HttpResponse


if not settings.configured:
    settings.configure(
        DEBUG=True,
        SECRET_KEY="uzbekiston-viloyatlari-secret",
        ROOT_URLCONF=__name__,       
        ALLOWED_HOSTS=["*"],
    )

def greet_viloyat(request, viloyat_name):
    """URL parametr orqali: /viloyat/Toshkent/"""
    return HttpResponse(f"Hi {viloyat_name}!")


def greet_query(request):
    """Query-param orqali: /salom/?name=Samarqand"""
    viloyat_name = request.GET.get("name", "Noma'lum")
    return HttpResponse(f"Hi {viloyat_name}!")


def home(request):
    html = """
    <h2>Viloyat Greeting App</h2>
    <ul>
      <li><a href="/viloyat/Toshkent/">URL param: /viloyat/Toshkent/</a></li>
      <li><a href="/viloyat/Samarqand/">URL param: /viloyat/Samarqand/</a></li>
      <li><a href="/salom/?name=Farg'ona">Query param: /salom/?name=Farg'ona</a></li>
    </ul>
    """
    return HttpResponse(html)



urlpatterns = [
    path("", home),
    path("viloyat/<str:viloyat_name>/", greet_viloyat, name="greet_viloyat"),
    path("salom/", greet_query, name="greet_query"),
]



if __name__ == "__main__":
    django.setup()
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv if len(sys.argv) > 1 else ["viloyat_app.py", "runserver"])