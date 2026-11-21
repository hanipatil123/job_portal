
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from .models import EmployerProfile, Job

User = get_user_model()


# ==========================================
# EMPLOYER REGISTRATION FORM
# ==========================================

class EmployerRegistrationForm(UserCreationForm):

    email = forms.EmailField(required=True)

    company_name = forms.CharField(
        max_length=150,
        required=True
    )

    company_email = forms.EmailField(required=True)

    company_phone = forms.CharField(
        max_length=15,
        required=True
    )

    class Meta(UserCreationForm.Meta):
        model = User

        fields = [
            "username",
            "email",
            "company_name",
            "company_email",
            "company_phone",
            "password1",
            "password2",
        ]

    def clean_email(self):
        email = self.cleaned_data["email"]

        if User.objects.filter(
            email__iexact=email
        ).exists():
            raise forms.ValidationError(
                "This email is already registered."
            )

        return email

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]

        if commit:
            user.save()

            EmployerProfile.objects.create(
                user=user,
                company_name=self.cleaned_data["company_name"],
                company_email=self.cleaned_data["company_email"],
                company_phone=self.cleaned_data["company_phone"],
            )

        return user


# ==========================================
# COMPANY PROFILE FORM
# ==========================================

class EmployerProfileForm(forms.ModelForm):

    class Meta:
        model = EmployerProfile

        fields = [
            "company_name",
            "company_email",
            "company_phone",
            "company_address",
            "company_description",
        ]

        widgets = {
            "company_address": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": "Enter company address"
                }
            ),

            "company_description": forms.Textarea(
                attrs={
                    "rows": 4,
                    "placeholder": "Describe your company"
                }
            ),
        }


# ==========================================
# POST NEW JOB / EDIT JOB FORM
# ==========================================

class JobForm(forms.ModelForm):

    application_deadline = forms.DateField(
        required=False,
        input_formats=["%Y-%m-%d"],
        widget=forms.DateInput(
            format="%Y-%m-%d",
            attrs={"type": "date"}
        )
    )

    class Meta:
        model = Job

        fields = [
            "title",
            "company_name",
            "location",
            "job_type",
            "salary",
            "experience",
            "vacancies",
            "qualification",
            "skills_required",
            "application_deadline",
            "description",
            "requirements",
        ]

        labels = {
            "title": "Job Title",
            "company_name": "Company Name",
            "location": "Job Location",
            "job_type": "Job Type",
            "salary": "Salary",
            "experience": "Experience Required",
            "vacancies": "Number of Vacancies",
            "qualification": "Educational Qualification",
            "skills_required": "Skills Required",
            "application_deadline": "Application Deadline",
            "description": "Job Description",
            "requirements": "Job Requirements",
        }

        widgets = {
            "title": forms.TextInput(
                attrs={
                    "placeholder": "e.g. Python Django Developer"
                }
            ),

            "company_name": forms.TextInput(
                attrs={
                    "placeholder": "e.g. TechNova Solutions"
                }
            ),

            "location": forms.TextInput(
                attrs={
                    "placeholder": "e.g. Pune, Maharashtra"
                }
            ),

            "salary": forms.TextInput(
                attrs={
                    "placeholder": "e.g. Rs. 25000 per month"
                }
            ),

            "experience": forms.TextInput(
                attrs={
                    "placeholder": "e.g. Fresher (0-1 Year)"
                }
            ),

            "vacancies": forms.NumberInput(
                attrs={"min": 1}
            ),

            "qualification": forms.TextInput(
                attrs={
                    "placeholder": "e.g. B.Tech / BCA / B.Sc."
                }
            ),

            "skills_required": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": "Python, Django, HTML, CSS, SQL"
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "rows": 5,
                    "placeholder": "Enter job responsibilities"
                }
            ),

            "requirements": forms.Textarea(
                attrs={
                    "rows": 4,
                    "placeholder": "Enter job requirements"
                }
            ),
        }

    def clean_vacancies(self):
        vacancies = self.cleaned_data["vacancies"]

        if vacancies < 1:
            raise forms.ValidationError(
                "Vacancies must be at least 1."
            )

        return vacancies
