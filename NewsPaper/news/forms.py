from django.forms import ModelForm, TextInput, Textarea

from .models import Post


class PostForm(ModelForm):
   def __init__(self, *args, **kwargs):
       super().__init__(*args, **kwargs)
       self.fields['author'].empty_label = 'Автор не выбран'



   class Meta:
       model = Post
       fields = ['author','post_status', 'heading', 'text_post']
       widgets = {
           'text_post': Textarea(attrs={'cols': 150})
       }
       labels = {
           'author': 'Выбор автора',
           'post_status': 'Выбор вида (новость/статья)',
           'heading': 'Название статьи',
           'text_post': 'Текст новости/статьи',

       }



