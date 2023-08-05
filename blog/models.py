from django.db import models
from django.db.models.query import QuerySet
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib import admin
from django.utils.html import format_html

class PublishedManager(models.Manager):
    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)

class Post(models.Model):

    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    title = models.CharField(max_length=250, verbose_name='Заголовок')
    slug = models.SlugField(max_length=250)
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='blog_posts',
                               verbose_name='Автор')

    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2,
                              choices=Status.choices,
                              default=Status.DRAFT,
                              verbose_name='Статус')
    
    objects = models.Manager()
    published = PublishedManager()
    
    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish'])
        ]
    
    def __str__(self):
        return self.title

    # Создаем функцию для столбца 'Дата создания' админки
    @admin.display(description='Дата создания')
    def vw_created(self):
        from django.utils import timezone
        if self.created.date() == timezone.now().date():
            created = self.created.time().strftime("%H:%M:%S")
            return format_html(
                '<span style="color: green; font-weight: bold;">Сегодня в {}</span>', created
            )
        return self.created.strftime("%d.%m.%Y в %H:%M:%S")
    
    @admin.display(description='Дата публикации')
    def vw_publish(self):
        from django.utils import timezone
        if self.publish.date() == timezone.now().date():
            publish = self.publish.time().strftime("%H:%M:%S")
            return format_html(
                '<span style="color: yellow; font-weight: bold;">Сегодня в {}</span>', publish
            )
        return self.publish.strftime("%d.%m.%Y в %H:%M:%S")
    
    @admin.display(description='Дата обновления')
    def vw_updated(self):
        from django.utils import timezone
        if self.updated.date() == timezone.now().date():
            updated = self.updated.time().strftime("%H:%M:%S")
            return format_html(
                '<span style="color: orange; font-weight: bold;">Сегодня в {}</span>', updated
            )
        return self.updated.strftime("%d.%m.%Y в %H:%M:%S")
   