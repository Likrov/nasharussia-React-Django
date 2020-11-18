import random
from django.conf import settings
from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url

from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from ..forms import Nash_messageForm
from ..models import Nash_message
from ..serializers import (
    Nash_messageSerializer, 
    Nash_messageActionSerializer,
    Nash_messageCreateSerializer
)

ALLOWED_HOSTS = settings.ALLOWED_HOSTS

@api_view(['POST']) # http method the client == POST
# @authentication_classes([SessionAuthentication, MyCustomAuth])
@permission_classes([IsAuthenticated]) # REST API course
def nash_message_create_view(request, *args, **kwargs):
    serializer = Nash_messageCreateSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user)
        return Response(serializer.data, status=201)
    return Response({}, status=400)

@api_view(['GET'])
def nash_message_detail_view(request, nash_message_id, *args, **kwargs):
    qs = Nash_message.objects.filter(id=nash_message_id)
    if not qs.exists():
        return Response({}, status=404)
    obj = qs.first()
    serializer = Nash_messageSerializer(obj)
    return Response(serializer.data, status=200)

@api_view(['DELETE', 'POST'])
@permission_classes([IsAuthenticated])
def nash_message_delete_view(request, nash_message_id, *args, **kwargs):
    qs = Nash_message.objects.filter(id=nash_message_id)
    if not qs.exists():
        return Response({}, status=404)
    qs = qs.filter(user=request.user)
    if not qs.exists():
        return Response({"message": "You cannot delete this nash_message"}, status=401)
    obj = qs.first()
    obj.delete()
    return Response({"message": "Nash_message removed"}, status=200)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def nash_message_action_view(request, *args, **kwargs):
    '''
    id is required.
    Action options are: like, unlike, renash
    '''
    serializer = Nash_messageActionSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        data = serializer.validated_data
        nash_message_id = data.get("id")
        action = data.get("action")
        content = data.get("content")
        qs = Nash_message.objects.filter(id=nash_message_id)
        if not qs.exists():
            return Response({}, status=404)
        obj = qs.first()
        if action == "like":
            obj.likes.add(request.user)
            serializer = Nash_messageSerializer(obj)
            return Response(serializer.data, status=200)
        elif action == "unlike":
            obj.likes.remove(request.user)
            serializer = Nash_messageSerializer(obj)
            return Response(serializer.data, status=200)
        elif action == "renash":
            new_nash_message = Nash_message.objects.create(
                    user=request.user, 
                    parent=obj,
                    content=content,
                    )
            serializer = Nash_messageSerializer(new_nash_message)
            return Response(serializer.data, status=201)
    return Response({}, status=200)


def get_paginated_queryset_response(qs, request):
    paginator = PageNumberPagination()
    paginator.page_size = 20
    paginated_qs = paginator.paginate_queryset(qs, request)
    serializer = Nash_messageSerializer(paginated_qs, many=True, context={"request": request})
    return paginator.get_paginated_response(serializer.data) # Response( serializer.data, status=200)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def nash_message_feed_view(request, *args, **kwargs):
    user = request.user
    qs = Nash_message.objects.feed(user)
    return get_paginated_queryset_response(qs, request)

@api_view(['GET'])
def nash_message_list_view(request, *args, **kwargs):
    qs = Nash_message.objects.all()
    username = request.GET.get('username') # ?username=Justin
    if username != None:
        qs = qs.by_username(username)
    return get_paginated_queryset_response(qs, request)



def nash_message_create_view_pure_django(request, *args, **kwargs):
    '''
    REST API Create View -> DRF
    '''
    user = request.user
    if not request.user.is_authenticated:
        user = None
        if request.is_ajax():
            return JsonResponse({}, status=401)
        return redirect(settings.LOGIN_URL)
    form = Nash_messageForm(request.POST or None)
    next_url = request.POST.get("next") or None
    if form.is_valid():
        obj = form.save(commit=False)
        # do other form related logic
        obj.user = user
        obj.save()
        if request.is_ajax():
            return JsonResponse(obj.serialize(), status=201) # 201 == created items
        if next_url != None and is_safe_url(next_url, ALLOWED_HOSTS):
            return redirect(next_url)
        form = Nash_messageForm()
    if form.errors:
        if request.is_ajax():
            return JsonResponse(form.errors, status=400)
    return render(request, 'components/form.html', context={"form": form})


def nash_message_list_view_pure_django(request, *args, **kwargs):
    """
    REST API VIEW
    Consume by JavaScript or Swift/Java/iOS/Andriod
    return json data
    """
    qs = Nash_message.objects.all()
    nash-message_list = [x.serialize() for x in qs]
    data = {
        "isUser": False,
        "response": nash-message_list
    }
    return JsonResponse(data)


def nash_message_detail_view_pure_django(request, nash_message_id, *args, **kwargs):
    """
    REST API VIEW
    Consume by JavaScript or Swift/Java/iOS/Andriod
    return json data
    """
    data = {
        "id": nash_message_id,
    }
    status = 200
    try:
        obj = Nash_message.objects.get(id=nash_message_id)
        data['content'] = obj.content
    except:
        data['message'] = "Not found"
        status = 404
    return JsonResponse(data, status=status) # json.dumps content_type='application/json'