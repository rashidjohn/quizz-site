from django.contrib import admin
from .models import Category, Test, Question, CheckQuestion,CheckTest

# Register your models here.

class QuestionInline(admin.TabularInline):
    model = Question

class TestAdmin(admin.ModelAdmin):
    inlines = [QuestionInline, ]
    list_display = ['title','author']

admin.site.register([Category,Question])
admin.site.register(Test,TestAdmin)
admin.site.register(CheckQuestion)
admin.site.register(CheckTest)