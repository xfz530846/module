from django.contrib import admin

# Register your models here.
from questions.models import Questions, AskLables, Answers, AnswersComments

admin.site.register(Questions)
admin.site.register(AskLables)
admin.site.register(Answers)
admin.site.register(AnswersComments)
# admin.site.register(AskLables)
