from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from app.models import Question, Answer, Profile
from django.http import Http404, HttpResponseRedirect
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.models import Tag
from django.utils import timezone
from .forms import add_post


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

    users = User.objects.all()
    profiles = Profile.objects.all()

    return render(request, 'index.html', {'questions': questions,
                                               'title': title, 'answers': answers,
                                               'users': users, 'profiles': profiles})


def question_page(request, qid):
    questions = get_object_or_404(Question, pk=qid)
    answers = {}
    answers[questions.id] = Answer.objects.filter(question=questions.id).count()
    comments = Answer.objects.get_queryset().filter(question=qid).order_by('create_date')
    comments = paginate(comments, request, 5)
    users = User.objects.all()
    profiles = Profile.objects.all()
    return render(request, 'question.html', {
        'question': questions, 'comments': comments,
        'users': users, 'profiles': profiles, 'answers': answers
    })


def signup(request):
    return render(request, 'signup.html', {

    })


def ask_question(request):
    if request.method == "POST":
        form = add_post(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author_id = request.user
            question.save()
            form.save_m2m()
            return HttpResponseRedirect(reverse('question_page', args=[question.id]))
    else:
        form = add_post()
    return render(request, 'index.html')


def create_post(request):
    form = add_post()
    return render(request, 'create_post.html', {'form': form})


def create_accounts_add(request):
    user = User.objects.create_user(username=request.POST['username'], email=request.POST['email'],
                                    password=request.POST['Password'], first_name=request.POST['firstName'],
                                    last_name=request.POST['lastName'])
    user.save()
    profile = Profile.objects.create(user=user, img=request.POST['img'])
    profile.save()
    return HttpResponseRedirect(reverse('login'))


def leave_answer(request, qid):
    question = get_object_or_404(Question, pk=qid)
    question.answer_set.create(author_id=request.user, text=request.POST['text'], create_date=timezone.now())
    return HttpResponseRedirect(reverse('question_page', args=[question.id]))


def user_profile_done(request):
    user = User.objects.get(username=request.user)
    user.username = request.POST.get("username")
    user.email = request.POST.get("email")
    user.first_name = request.POST.get("firstName")
    user.last_name = request.POST.get("lastName")
    user.save()
    return HttpResponseRedirect(reverse('index'))


def user_profile(request):
    return render(request, 'user_profile.html')
