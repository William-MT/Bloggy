from django.forms import ModelForm
from .models import Post, Message


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
        exclude = ['user', 'participants']


class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = '__all__'
        exclude = []