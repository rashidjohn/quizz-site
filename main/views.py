from django.shortcuts import render, get_object_or_404, redirect
from .models import Test, Question, CheckQuestion, CheckTest
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils import timezone
from .forms import QuestionForm, TestForm

# Create your views here.

def index(request):
    tests = Test.objects.all()
    return render(request, 'index.html', {'tests':tests})

@login_required(login_url='login')
def ready_to_test(request, test_id):
    test = get_object_or_404(Test, id=test_id)
    return render(request, 'ready_to_test.html', {'test':test})

@login_required(login_url='login')
def test(request, test_id):
    test = get_object_or_404(Test, id=test_id)
    attemps = CheckTest.objects.filter(student=request.user, test=test).count()
    if (timezone.now()>=test.start_date and timezone.now() <= test.end_date ) and attemps < test.maximum_attemps:    
        questions = Question.objects.filter(test=test)
        if request.method=='POST':
            checktest = CheckTest.objects.create(student=request.user, test=test)
            for question in questions:
                given_answer = request.POST[str(question.id)]
                CheckQuestion.objects.create(checktest=checktest, question=question,given_answer=given_answer, true_answer=question.true_answer)
            checktest.save()
            return redirect('checktest', checktest.id)
        context = {'test':test, 'questions':questions}
        return render(request, 'test.html', context)
    else:
        return HttpResponse('Test not Found!')
    
@login_required(login_url='login')
def checktest(request, checktest_id):
    checktest = get_object_or_404(CheckTest, id=checktest_id, student=request.user)
    return render(request, 'checktest.html', {'checktest':checktest})

@login_required(login_url='login')
def new_test(request):
    form = TestForm()
    if request.method == 'POST':
        form = TestForm(data=request.POST)
        if form.is_valid:
            test = form.save(commit=False)
            test.author = request.user
            test.save()
            test_id = test.pk
            return redirect('new_question', test_id)
    return render(request, 'new_test.html', {'form':form})
@login_required(login_url='login')
def new_question(request, test_id):
    test = get_object_or_404(Test, id=test_id)
    if test.author == request.user:
        form = QuestionForm()
        if request.method == 'POST':
            form = QuestionForm(data=request.POST)
            if form.is_valid:
                form.save(test_id)
                if form.cleaned_data['submit_and_exit']:
                    return redirect('index')
                return redirect('new_question', test_id)
        return render(request, 'new_question.html', {'form':form,'test':test})
    else:
        return HttpResponse('Something Went Wrong!!!')