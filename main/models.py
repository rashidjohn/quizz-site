from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.signals import pre_save
from django.dispatch import receiver

class Category(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name

class Test(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    maximum_attemps = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(default=timezone.now() + timezone.timedelta(days=10))
    pass_percentage = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])

    def __str__(self):
        return self.title

class Question(models.Model):
    ANSWER_CHOICES = [('a', 'A'), ('b', 'B'), ('c', 'C'), ('d', 'D')]
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    question = models.CharField(max_length=300)
    a = models.CharField(max_length=150)
    b = models.CharField(max_length=150)
    c = models.CharField(max_length=150)
    d = models.CharField(max_length=150)
    true_answer = models.CharField(max_length=1, choices=ANSWER_CHOICES, help_text='E.g., a')

    def __str__(self):
        return self.question

class CheckTest(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    finded_questions = models.PositiveIntegerField(default=0)
    user_passed = models.BooleanField(default=False)
    percentage = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'Test of {self.student.username}'

class CheckQuestion(models.Model):
    checktest = models.ForeignKey(CheckTest, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    given_answer = models.CharField(max_length=1, help_text='E.g., a')
    true_answer = models.CharField(max_length=1, help_text='E.g., a')
    is_true = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.question.question} solved by {self.checktest.student.username}'

@receiver(pre_save, sender=CheckQuestion)
def check_answer(sender, instance, *args, **kwargs):
    instance.is_true = instance.given_answer == instance.true_answer

@receiver(pre_save, sender=CheckTest)
def check_test(sender, instance, *args, **kwargs):
    checktest = instance
    try:
        total_questions = CheckQuestion.objects.filter(checktest=checktest).count()
        correct_questions = CheckQuestion.objects.filter(checktest=checktest, is_true=True).count()
        checktest.finded_questions = correct_questions
        if total_questions > 0:
            checktest.percentage = (correct_questions * 100) // total_questions
            checktest.user_passed = checktest.percentage >= checktest.test.pass_percentage
    except Exception:
        checktest.percentage = 0
        checktest.user_passed = False