from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils import timezone
from django.contrib import messages
from .models import Test, Question, CheckQuestion, CheckTest
from .forms import QuestionForm, TestForm

def index(request):
    tests = Test.objects.all()
    return render(request, 'index.html', {'tests': tests})

@login_required(login_url='login')
def ready_to_test(request, test_id):
    test = get_object_or_404(Test, id=test_id)
    return render(request, 'ready_to_test.html', {'test': test})

@login_required(login_url='login')
def test(request, test_id):
    test = get_object_or_404(Test, id=test_id)
    attempts = CheckTest.objects.filter(student=request.user, test=test).count()
    if not (test.start_date <= timezone.now() <= test.end_date):
        messages.error(request, 'This test is not available at this time.')
        return render(request, 'error.html', {'message': 'Test is not available.'})
    if attempts >= test.maximum_attemps:
        messages.error(request, 'You have reached the maximum number of attempts.')
        return render(request, 'error.html', {'message': 'Maximum attempts reached.'})
    
    questions = Question.objects.filter(test=test)
    if not questions.exists():
        messages.error(request, 'No questions available for this test.')
        return render(request, 'error.html', {'message': 'No questions available.'})
    
    if request.method == 'POST':
        checktest = CheckTest.objects.create(student=request.user, test=test)
        for question in questions:
            given_answer = request.POST.get(str(question.id), '')
            if given_answer in ['a', 'b', 'c', 'd']:
                CheckQuestion.objects.create(
                    checktest=checktest,
                    question=question,
                    given_answer=given_answer,
                    true_answer=question.true_answer
                )
        checktest.save()
        messages.success(request, 'Test submitted successfully!')
        return redirect('checktest', checktest.id)
    
    return render(request, 'test.html', {'test': test, 'questions': questions})

@login_required(login_url='login')
def checktest(request, checktest_id):
    checktest = get_object_or_404(CheckTest, id=checktest_id, student=request.user)
    return render(request, 'checktest.html', {'checktest': checktest})

@login_required(login_url='login')
def new_test(request):
    if request.method == 'POST':
        form = TestForm(request.POST)
        if form.is_valid():
            test = form.save(user=request.user)
            messages.success(request, 'Test created successfully!')
            return redirect('new_question', test.id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = TestForm()
    return render(request, 'new_test.html', {'form': form})

@login_required(login_url='login')
def new_question(request, test_id):
    test = get_object_or_404(Test, id=test_id)
    if test.author != request.user:
        messages.error(request, 'You are not authorized to add questions to this test.')
        return render(request, 'error.html', {'message': 'Unauthorized access.'})
    
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save(test_id=test_id)
            messages.success(request, 'Question added successfully!')
            if form.cleaned_data['submit_and_exit']:
                return redirect('index')
            return redirect('new_question', test_id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = QuestionForm()
    return render(request, 'new_question.html', {'form': form, 'test': test})