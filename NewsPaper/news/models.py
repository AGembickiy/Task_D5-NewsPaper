from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import Sum
# Create your models here.

User = get_user_model()


class Author(models.Model):
    rating_author = models.IntegerField(default=0)
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    def update_rating(self):
        # суммарный рейтинг каждой статьи автора умножается на 3
        rating_post = self.posts.all().values('rating_post')
        rating_post = rating_post.aggregate(Sum('rating_post'))['rating_post__sum']*3

        # суммарный рейтинг всех комментариев автора
        rating_comments = self.user.users.all().values('rating_comment')
        rating_comments = rating_comments.aggregate(Sum('rating_comment'))['rating_comment__sum']

        # суммарный рейтинг всех комментариев к статьям автора
        rating_comments_articles = self.posts.all()
        rating_comments_articles = list(map(lambda n: n.posts.values('rating_comment'), rating_comments_articles))
        rating_comments_articles = rating_comments_articles[0].aggregate(Sum('rating_comment'))['rating_comment__sum']

        self.rating_author = rating_post + rating_comments + rating_comments_articles

        return self.rating_author

    def __str__(self):
        # f'Имя автара: {self.user.username}\nРейтинг автара: {self.rating_author}'
        return f'{self.user.first_name} {self.user.last_name}'

class Category(models.Model):
    topic = models.CharField(max_length=100, unique=True)

class Post(models.Model):
    AR = 'AR'
    NE = 'NE'
    ARTICLE_OR_NEWS_SELECTION_FIELD = {
        AR: 'Статья',
        NE: 'Новость',
    }
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='posts')
    post_status =  models.CharField(
        max_length=2,
        choices=ARTICLE_OR_NEWS_SELECTION_FIELD,
        default=AR
    )
    post_category = models.CharField(max_length=20)
    date_time_creation = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(
        Category,
        through="PostCategory"
    )

    heading = models.CharField(
        max_length=64,
    )
    text_post = models.TextField()
    rating_post = models.IntegerField(default=0)

    def like(self):
        self.rating_post += 1
        return self.rating_post
    def dislike(self):
        if self.rating_post > 0:
            self.rating_post -= 1
            return self.rating_post
        return self.rating_post

    def preview(self):
        if len(self.text_post)>125:
            result = f'{self.text_post[0:125]}...'
            return result
        return self.text_post

    def get_absolute_url(self):
        return f'/news/{self.id}'

    def __str__(self):

        return (f'Дата создания: {self.date_time_creation.strftime('%d.%b.%Y %H:%M')}\n'
                f'Автор: {self.author.user.username}\n'
                f'Рейтинг автора: {self.author.rating_author}\n'
                f'Заголовок: {self.heading}\n'
                f'Превью: {self.preview()}')


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)




class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='posts')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='users')
    text_comment = models.TextField()
    date_time_comment = models.DateTimeField(auto_now_add=True)
    rating_comment = models.IntegerField(default=0)

    def like(self):
        self.rating_comment += 1
        return self.rating_comment

    def dislike(self):
        if self.rating_comment > 0:
            self.rating_comment -= 1
            return self.rating_comment
        return self.rating_comment

    def __str__(self):
        return (f'Дата создания коментария: {self.date_time_comment.strftime('%d.%b.%Y %H:%M')}\n'
                f'Имя пользователя: {self.user.username}\n'
                f'Рейтинг: {self.rating_comment}\n'
                f'Текст коментария: {self.text_comment}')

