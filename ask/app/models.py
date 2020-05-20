from __future__ import unicode_literals

from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from taggit.managers import TaggableManager
from django.db.models import Sum
from django.utils import timezone
from taggit.models import Tag


class Question(models.Model):
    title = models.CharField(default='', max_length=120, verbose_name=u"Заголовок вопроса")
    text = models.TextField(default='', verbose_name=u"Полное описание вопроса")
    create_date = models.DateTimeField(default=datetime.now, verbose_name=u"Время создания вопроса")
    is_active = models.BooleanField(default=True, verbose_name=u"Доступность вопроса")
    author_id = models.ForeignKey(User,  on_delete=models.CASCADE)

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
    author_id = models.ForeignKey(User, on_delete=models.CASCADE)
    create_date = models.DateTimeField(default=datetime.now, verbose_name=u"дата публикации")

    def answer_to_questions(self, question_id):
        return self.objects.get_queryset().filter(question=question_id).order_by('create_date')


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    img = models.ImageField(default='default.jpg', upload_to='user_images')

