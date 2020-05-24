from __future__ import unicode_literals

from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from taggit.managers import TaggableManager
from taggit.models import Tag
from .manager import LikeDislikeManager


class Profile(AbstractUser):
    img = models.ImageField(default='avatar.jpg', upload_to='media')


class LikeDislike(models.Model):
    LIKE = 1
    DISLIKE = -1

    VOTES = (
        (DISLIKE, 'Не нравится'),
        (LIKE, 'Нравится')
    )

    vote = models.SmallIntegerField(verbose_name=u"Голос", choices=VOTES)
    user = models.ForeignKey(Profile, verbose_name=u"Пользователь", on_delete=models.CASCADE)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    objects = LikeDislikeManager()


class Article(models.Model):
    votes = GenericRelation(LikeDislike, related_query_name='articles')


class Comment(models.Model):
    votes = GenericRelation(LikeDislike, related_query_name='comments')


class Question(models.Model):
    title = models.CharField(default='', max_length=120, verbose_name=u"Заголовок вопроса")
    text = models.TextField(default='', verbose_name=u"Полное описание вопроса")
    create_date = models.DateTimeField(default=datetime.now, verbose_name=u"Время создания вопроса")
    is_active = models.BooleanField(default=True, verbose_name=u"Доступность вопроса")
    author_id = models.ForeignKey(Profile,  on_delete=models.CASCADE)

    tags = TaggableManager()

    def __unicode__(self):
        return self.title

    def answers_count(self):
        answers = {}
        for question in Question.objects.all():
            answers[question.id] = Answer.objects.filter(question=question.id).count()

    def new_questions(self):
        return self.objects.get_queryset().order_by('create_date')

    def new_tag_questions(self, tag_slug):
        posts = Question.new_questions(self)
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags__in=[tag])
        return posts

    def hottest_questions(self):
        return self.objects.all()

    class Meta:
        ordering = ['-create_date']


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.TextField(default='')
    author_id = models.ForeignKey(Profile, on_delete=models.CASCADE)
    create_date = models.DateTimeField(default=datetime.now, verbose_name=u"дата публикации")

    def answer_to_questions(self, question_id):
        return self.objects.get_queryset().filter(question=question_id).order_by('create_date')


