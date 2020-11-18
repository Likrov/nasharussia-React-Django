from django.contrib.auth import get_user_model
from django.test import TestCase

from rest_framework.test import APIClient

from .models import Nash_message
# Create your tests here.
User = get_user_model()

class Nash_messageTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='cfe', password='somepassword')
        self.userb = User.objects.create_user(username='cfe-2', password='somepassword2')
        Nash_message.objects.create(content="my first nash_message", 
            user=self.user)
        Nash_message.objects.create(content="my first nash_message", 
            user=self.user)
        Nash_message.objects.create(content="my first nash_message", 
            user=self.userb)
        self.currentCount = Nash_message.objects.all().count()

    def test_nash_message_created(self):
        nash_message_obj = Nash_message.objects.create(content="my second nash_message", 
            user=self.user)
        self.assertEqual(nash_message_obj.id, 4)
        self.assertEqual(nash_message_obj.user, self.user)
    
    def get_client(self):
        client = APIClient()
        client.login(username=self.user.username, password='somepassword')
        return client
    
    def test_nash_message_list(self):
        client = self.get_client()
        response = client.get("/api/nash-message/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    def test_nash_message_list(self):
        client = self.get_client()
        response = client.get("/api/nash-message/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 3)
    
    def test_nash-message_related_name(self):
        user = self.user
        self.assertEqual(user.nash-message.count(), 2)

    def test_action_like(self):
        client = self.get_client()
        response = client.post("/api/nash-message/action/", 
            {"id": 1, "action": "like"})
        like_count = response.json().get("likes")
        user = self.user
        my_like_instances_count = user.nash_messagelike_set.count()
        my_related_likes = user.nash_message_user.count()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(like_count, 1)
        self.assertEqual(my_like_instances_count, 1)
        self.assertEqual(my_like_instances_count, my_related_likes)
    
    def test_action_unlike(self):
        client = self.get_client()
        response = client.post("/api/nash-message/action/", 
            {"id": 2, "action": "like"})
        self.assertEqual(response.status_code, 200)
        response = client.post("/api/nash-message/action/", 
            {"id": 2, "action": "unlike"})
        self.assertEqual(response.status_code, 200)
        like_count = response.json().get("likes")
        self.assertEqual(like_count, 0)
    
    def test_action_renash(self):
        client = self.get_client()
        response = client.post("/api/nash-message/action/", 
            {"id": 2, "action": "renash"})
        self.assertEqual(response.status_code, 201)
        data = response.json()
        new_nash_message_id = data.get("id")
        self.assertNotEqual(2, new_nash_message_id)
        self.assertEqual(self.currentCount + 1, new_nash_message_id)

    def test_nash_message_create_api_view(self):
        request_data = {"content": "This is my test nash_message"}
        client = self.get_client()
        response = client.post("/api/nash-message/create/", request_data)
        self.assertEqual(response.status_code, 201)
        response_data = response.json()
        new_nash_message_id = response_data.get("id")
        self.assertEqual(self.currentCount + 1, new_nash_message_id)
    
    def test_nash_message_detail_api_view(self):
        client = self.get_client()
        response = client.get("/api/nash-message/1/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        _id = data.get("id")
        self.assertEqual(_id, 1)

    def test_nash_message_delete_api_view(self):
        client = self.get_client()
        response = client.delete("/api/nash-message/1/delete/")
        self.assertEqual(response.status_code, 200)
        client = self.get_client()
        response = client.delete("/api/nash-message/1/delete/")
        self.assertEqual(response.status_code, 404)
        response_incorrect_owner = client.delete("/api/nash-message/3/delete/")
        self.assertEqual(response_incorrect_owner.status_code, 401)