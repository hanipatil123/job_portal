from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from .models import JobSeekerProfile,JobApplication
class StyledForm:
 def style(self):
  for f in self.fields.values():f.widget.attrs.setdefault('class','form-control')
class RegisterForm(UserCreationForm,StyledForm):
 email=forms.EmailField(required=True)
 first_name=forms.CharField(max_length=100,required=True)
 last_name=forms.CharField(max_length=100,required=False)
 class Meta:
  model=User;fields=['first_name','last_name','username','email','password1','password2']
 def __init__(self,*args,**kwargs):
  super().__init__(*args,**kwargs);self.style()
 def clean_email(self):
  email=self.cleaned_data['email'].lower()
  if User.objects.filter(email__iexact=email).exists():raise forms.ValidationError('Email already registered.')
  return email
class LoginForm(AuthenticationForm,StyledForm):
 def __init__(self,*args,**kwargs):
  super().__init__(*args,**kwargs);self.style()
class ProfileForm(forms.ModelForm,StyledForm):
 first_name=forms.CharField(max_length=100,required=True)
 last_name=forms.CharField(max_length=100,required=False)
 email=forms.EmailField(required=True)
 class Meta:
  model=JobSeekerProfile;fields=['phone','location','headline','skills','experience','bio','resume']
  widgets={'bio':forms.Textarea(attrs={'rows':4}),'skills':forms.Textarea(attrs={'rows':3}),'resume':forms.ClearableFileInput(attrs={'accept':'.pdf,.doc,.docx'})}
 def __init__(self,*args,**kwargs):
  super().__init__(*args,**kwargs)
  if self.instance and self.instance.pk:
   u=self.instance.user
   self.fields['first_name'].initial=u.first_name;self.fields['last_name'].initial=u.last_name;self.fields['email'].initial=u.email
  self.style()
 def clean_email(self):
  email=self.cleaned_data['email'].lower()
  if User.objects.filter(email__iexact=email).exclude(pk=self.instance.user_id).exists():raise forms.ValidationError('Email already in use.')
  return email
 def clean_resume(self):
  file=self.cleaned_data.get('resume')
  if file and hasattr(file,'size') and file.size>5*1024*1024:raise forms.ValidationError('Resume must be 5 MB or less.')
  return file
 def save(self,commit=True):
  profile=super().save(commit=commit)
  u=profile.user;u.first_name=self.cleaned_data['first_name'];u.last_name=self.cleaned_data['last_name'];u.email=self.cleaned_data['email'];u.save()
  return profile
class ApplyForm(forms.ModelForm,StyledForm):
 class Meta:
  model=JobApplication;fields=['cover_letter'];widgets={'cover_letter':forms.Textarea(attrs={'rows':5,'placeholder':'Tell the employer why you are a great fit...'})}
 def __init__(self,*args,**kwargs):super().__init__(*args,**kwargs);self.style()
