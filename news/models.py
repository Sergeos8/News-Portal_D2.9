from datetime import datetime, timezone
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum

# Модель Author
class Author(models.Model):
    # Рейтинг пользователя, по умолчанию = 0
    user_rate = models.IntegerField(default=0)
    # Связь «один к одному»
    author = models.OneToOneField(User, on_delete=models.CASCADE)

    # Обновление рейтинга модели Author
    def update_rating(self):
        # Суммарный рейтинг всех комментариев к "Статьям" конкретной модели Author
        sum_rating = self.post_set.aggregate(post_rating=Sum('post_rate'))
        result_sum_rating = 0
        try:
            result_sum_rating += sum_rating.get('post_rating')
        except TypeError:
            result_sum_rating = 0

        # Суммарный рейтинг всех комментариев конкретной модели Author
        sum_comment_rating = self.author.comment_set.aggregate(comment_rating=Sum('comment_rate'))
        result_sum_comment_rating = 0
        result_sum_comment_rating += sum_comment_rating.get('comment_rating')

        # Суммарный рейтинг каждой "Статьи" модели Author, умноженный на 3
        self.user_rate = result_sum_rating * 3 + result_sum_comment_rating
        self.save()


# Модель категории "Новостей" / "Статей"
class Category(models.Model):
    article_category = models.CharField(max_length=255, unique=True)


# Модель Post
class Post(models.Model):
    # Поле со связью "Один ко многим" с моделью Author
    post_author = models.ForeignKey(Author, on_delete=models.CASCADE)
    # Поле со связью "Многие ко многим" с моделью Category
    post_category = models.ManyToManyField(Category)

    """ Настройка выбора категории поста """
    # Поле с выбором ("Статья" или "Новость")
    article = 'A'
    news = 'N'

    POSITIONS = [
        (article, "Статья"),
        (news, "Новость"),
    ]

    # Выбор категории модели Post ("Статья" или "Новость"), длина символа = 1, по умолчанию = "Новость"
    category = models.CharField(max_length=1,
                                choices=POSITIONS,
                                default=article)
    """ Конец настройки выбора категории поста """

    # Дата и время создания модели Post
    date_created = models.DateField(auto_now_add=True)

    # Заголовок "Статьи" / "Новости"
    title = models.CharField(max_length=128)

    # Текст "Статьи" / "Новости"
    content = models.TextField()

    """ Рейтинг """
    # Рейтинг "Статьи" / "Новости"
    post_rate = models.IntegerField(default=0)

    # Метод, увеличивающий рейтинг на единицу
    def like(self):
        self.post_rate += 1
        self.save()

    # Метод, уменьшающий рейтинг на единицу
    def dislike(self):
        self.post_rate -= 1
        self.save()

    # Предварительный просмотр "Статьи" (превью 124 символов статьи)
    def preview(self):
        return self.content[0:124] + "..."


#  Модель промежуточная PostCategory
class PostCategory(models.Model):
    # связь "Один ко многим" с моделью Post
    post_category = models.ForeignKey(Post, on_delete=models.CASCADE)
    # связь "Один ко многим" с моделью Category
    category_category = models.ManyToManyField(Category)


# Модель Comment, для комментирования "Новостей" / "Статьей"
class Comment(models.Model):
    # Связь «Один ко многим» с моделью Post
    comment_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    # Связь «Один ко многим» со встроенной моделью User (комментарии может оставить любой User)
    comment_user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Содержание комментария
    feedback_text = models.TextField()
    # Дата и время создания комментария
    comment_date_created = models.DateField(auto_now_add=True)
    # Рейтинг комментария
    comment_rate = models.IntegerField(default=0)

    # Метод, увеличивающий рейтинг на единицу
    def like(self):
        self.comment_rate += 1
        self.save()

    # Метод, уменьшающий рейтинг на единицу
    def dislike(self):
        self.comment_rate -= 1
