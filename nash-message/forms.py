from django.conf import settings
from django import forms

from .models import Nash_message

MAX_NASH_MESSAGE_LENGTH = settings.MAX_NASH_MESSAGE_LENGTH

class Nash_messageForm(forms.ModelForm):
    class Meta:
        model = Nash_message
        fields = ['content']
    
    def clean_content(self):
        content = self.cleaned_data.get("content")
        if len(content) > MAX_NASH_MESSAGE_LENGTH:
            raise forms.ValidationError("This nash_message is too long")
        return content