import random
from django.conf import settings
from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url


ALLOWED_HOSTS = settings.ALLOWED_HOSTS

# Create your views here.
def home_view(request, *args, **kwargs):
    return render(request, "pages/feed.html")

def nash-message_list_view(request, *args, **kwargs):
    return render(request, "nash-message/list.html")

def nash-message_detail_view(request, nash-message_id, *args, **kwargs):
    return render(request, "nash-message/detail.html", context={"nash-message_id": nash-message_id})
