
from django import forms
from .models import JobCategory, JobPosting


class JobCategoryForm(forms.ModelForm):
    class Meta:
        model = JobCategory
        fields = ['name', 'description']




class JobPostingForm(forms.ModelForm):
    class Meta:
        model = JobPosting
        fields = [
            'title',
            'employer',
            'category',
            'location',
            'salary',
            'description',
            'status'
        ]
