from django.contrib import admin
from .models import Question, QuestionOption, QuestionFileProperty, Response, Certificate

admin.site.register(Question)
admin.site.register(QuestionOption)
admin.site.register(QuestionFileProperty)
admin.site.register(Response)
admin.site.register(Certificate)
