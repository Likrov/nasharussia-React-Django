import random
from django.conf import settings
from django.db import models
from django.db.models import Q

User = settings.AUTH_USER_MODEL

class Nash_messageLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nash_message = models.ForeignKey("Nash_message", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

class Nash_messageQuerySet(models.QuerySet):
    def by_username(self, username):
        return self.filter(user__username__iexact=username)

    def feed(self, user):
        profiles_exist = user.following.exists()
        followed_users_id = []
        if profiles_exist:
            followed_users_id = user.following.values_list("user__id", flat=True) # [x.user.id for x in profiles]
        return self.filter(
            Q(user__id__in=followed_users_id) |
            Q(user=user)
        ).distinct().order_by("-timestamp")

class Nash_messageManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return Nash_messageQuerySet(self.model, using=self._db)

    def feed(self, user):
        return self.get_queryset().feed(user)

class Nash_message(models.Model):
    # Maps to SQL data
    # id = models.AutoField(primary_key=True)
    parent = models.ForeignKey("self", null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="nash-message") # many users can many nash-message
    likes = models.ManyToManyField(User, related_name='nash_message_user', blank=True, through=Nash_messageLike)
    content = models.TextField(blank=True, null=True)
    image = models.FileField(upload_to='images/', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = Nash_messageManager()
    # def __str__(self):
    #     return self.content
    
    class Meta:
        ordering = ['-id']
    
    @property
    def is_renash(self):
        return self.parent != None
    
    def serialize(self):
        '''
        Feel free to delete!
        '''
        return {
            "id": self.id,
            "content": self.content,
            "likes": random.randint(0, 200)
        }