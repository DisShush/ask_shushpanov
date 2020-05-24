from django.contrib import admin

from .models import Question, Answer, Profile


admin.site.register(Question)
admin.site.register(Profile)
admin.site.register(Answer)
