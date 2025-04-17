from django import forms
from .models import Test, Question

class TestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ('title', 'category', 'maximum_attemps', 'start_date', 'end_date', 'pass_percentage')
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def save(self, user, commit=True):
        test = super().save(commit=False)
        test.author = user
        if commit:
            test.save()
        return test

class QuestionForm(forms.ModelForm):
    submit_and_exit = forms.BooleanField(required=False, label='Save and Exit')

    class Meta:
        model = Question
        fields = ('question', 'a', 'b', 'c', 'd', 'true_answer')
        widgets = {
            'true_answer': forms.Select(choices=[('a', 'A'), ('b', 'B'), ('c', 'C'), ('d', 'D')]),
        }

    def clean_true_answer(self):
        true_answer = self.cleaned_data.get('true_answer')
        if true_answer not in ['a', 'b', 'c', 'd']:
            raise forms.ValidationError('True answer must be one of: a, b, c, d.')
        return true_answer

    def save(self, test_id, commit=True):
        question = super().save(commit=False)
        question.test_id = test_id
        if commit:
            question.save()
        return question