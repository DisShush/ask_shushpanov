from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from app.models import Question, Answer, Profile
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.models import Tag
from django.utils import timezone
from .forms import *
from django.views import View
from django.contrib.contenttypes.models import ContentType
from .models import LikeDislike
from django.core.files.storage import FileSystemStorage


def paginate(objects_list, request, obj_per_list=2):
    paginator = Paginator(objects_list, obj_per_list)
    page = request.GET.get('page')
    items = paginator.get_page(page)
    return items


def index(request, tag_slug=None):
    posts = Question.objects.all()
    title = 'Recent updates'
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags__in=[tag])
        title = '#' + str(tag)
    questions = paginate(posts, request, 10)
    answers = {}
    for question in Question.objects.all():
        answers[question.id] = Answer.objects.filter(question=question.id).count()

    profiles = Profile.objects.all()
    return render(request, 'index.html', {'questions': questions,
                                            'title': title, 'answers': answers,
                                            'profiles': profiles})


class CreateAccount(View):
    def get(self, request):
        form = add_register()
        return render(request, 'signup.html', {'form': form})

    def post(self, request):
        form = add_register(request.POST, request.FILES)
        if form.is_valid():
            acc = form.save(commit=False)
            form.save()
            acc.set_password(acc.password)
            acc.is_active = True
            acc.save()
            return HttpResponseRedirect(reverse('login'))
        return HttpResponseRedirect(reverse('signup'))


class SettingProfile(View):
        def get(self, request):
            curr_acc = Profile.objects.get(username=request.user)
            form = setting_profile(instance=curr_acc)
            return render(request, 'user_profile.html', {'form': form})

        def post(self, request):
            form = setting_profile(request.POST, request.FILES)
            if form.is_valid():
                user = Profile.objects.get(username=request.user)
                user.email = form.data.get("email")
                user.first_name = form.data.get("first_name")
                user.last_name = form.data.get("last_name")
                user.img = form.files.get("img", default=user.img)
                user.save()
                return HttpResponseRedirect(reverse('index'))
            return HttpResponseRedirect(reverse('user_profile'))


class CreatePost(View):
    def get(self, request):
        form = add_post()
        return render(request, 'create_post.html', {'form': form})

    def post(self, request):
        if request.method == "POST":
            form = add_post(request.POST)
            if form.is_valid():
                question = form.save(commit=False)
                question.author_id = request.user
                question.save()
                form.save_m2m()
                return HttpResponseRedirect(reverse('question_page', args=[question.id]))
            return render(request, 'index.html')


class Questions(View):
    def get(self, request, qid):
        form = add_answer()
        questions = get_object_or_404(Question, pk=qid)
        answers = {}
        answers[questions.id] = Answer.objects.filter(question=questions.id).count()
        comments = Answer.objects.get_queryset().filter(question=qid).order_by('create_date')
        comments = paginate(comments, request, 5)
        users = Profile.objects.all()
        profiles = Profile.objects.all()
        return render(request, 'question.html', {
            'question': questions, 'comments': comments,
            'users': users, 'profiles': profiles, 'answers': answers,
            'form': form,
        })

    def post(self, request, qid):
        question = get_object_or_404(Question, pk=qid)
        if request.method == "POST":
            form = add_answer(request.POST)
            if form.is_valid():
                answer = form.save(commit=False)
                answer.author_id = request.user
                answer.question = question
                answer.save()
                form.save_m2m()
                return HttpResponseRedirect(reverse('question_page', args=[question.id]))
            return HttpResponseRedirect(reverse('index'))

