from django.urls import path

from .views import (
    nash_message_action_view,
    nash_message_delete_view,
    nash_message_detail_view,
    nash_message_feed_view,
    nash_message_list_view,
    nash_message_create_view,
)
'''
CLIENT
Base ENDPOINT /api/nash-message/
'''
urlpatterns = [
    path('', nash_message_list_view),
    path('feed/', nash_message_feed_view),
    path('action/', nash_message_action_view),
    path('create/', nash_message_create_view),
    path('<int:nash_message_id>/', nash_message_detail_view),
    path('<int:nash_message_id>/delete/', nash_message_delete_view),
]
