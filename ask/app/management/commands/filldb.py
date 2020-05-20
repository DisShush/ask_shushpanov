from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone

from app.models import Question, Answer, Profile
from random import choice
from faker import Faker
from taggit.models import Tag

f = Faker()


class Command(BaseCommand):

    def fill_authors(self, cnt):
        for i in range(cnt):
           user = User.objects.create(password=f.password(), username=f.name(), email=f.email())
           user.save()
           profile = Profile.objects.create(user=user)
           profile.save()

    def fill_questions(self, cnt):
        tags = ['python', 'news', 'case', 'tutorial', 'analytics', 'help', 'error']
        author_ids = list(
            User.objects.values_list(
                'id', flat=True
            )
        )

        for i in range(cnt):
            q = Question.objects.create(
                author_id=User.objects.get(id=choice(author_ids)),
                title=f.sentence()[:128],
                text=f.sentence()[:256],
                create_date=timezone.now()
            )
            for _ in range(f.random_int(min=2, max=5)):
                 q.tags.add(tags[f.random_int(min=0, max=3)])


    def fill_answers(self, cnt):
        author_ids = list(
            User.objects.values_list(
                'id', flat=True
            )
        )
        questions_ids = list(
            Question.objects.values_list(
                'id', flat=True
            )
        )
        for i in range(cnt):
            Answer.objects.create(
                author_id=User.objects.get(id=choice(author_ids)),
                question=Question.objects.get(id=choice(questions_ids)),
                text=f.sentence()[:256],
                create_date=timezone.now()
            )


    def handle(self, *args, **options):
        self.fill_authors(options.get('authors', 5))
        self.fill_questions(options.get('questions', 20))
        self.fill_answers(options.get('answers', 100))
