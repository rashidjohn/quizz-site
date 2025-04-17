from django.contrib import admin
from .models import Category, Test, Question, CheckQuestion, CheckTest

# Inline for Questions in TestAdmin
class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1

# Test Admin Configuration
class TestAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]
    list_display = ['title', 'author', 'category', 'start_date', 'end_date']
    search_fields = ['title', 'author__username']
    list_filter = ['category', 'start_date']

# Category Admin Configuration
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

# CheckQuestion Admin Configuration
class CheckQuestionAdmin(admin.ModelAdmin):
    list_display = ['question', 'checktest', 'given_answer', 'is_true']
    list_filter = ['is_true', 'checktest__test']
    search_fields = ['question__question']

# CheckTest Admin Configuration
class CheckTestAdmin(admin.ModelAdmin):
    list_display = ['student', 'test', 'percentage', 'user_passed']
    list_filter = ['user_passed', 'test']
    search_fields = ['student__username', 'test__title']

# Register models
admin.site.register(Category, CategoryAdmin)
admin.site.register(Test, TestAdmin)
admin.site.register(Question)
admin.site.register(CheckQuestion, CheckQuestionAdmin)
admin.site.register(CheckTest, CheckTestAdmin)