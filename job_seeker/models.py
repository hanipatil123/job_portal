from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
class JobSeekerProfile(models.Model):
 user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='seeker_profile')
 phone=models.CharField(max_length=20,blank=True)
 location=models.CharField(max_length=120,blank=True)
 headline=models.CharField(max_length=160,blank=True)
 skills=models.TextField(blank=True)
 bio=models.TextField(blank=True)
 experience=models.CharField(max_length=40,blank=True)
 resume=models.FileField(upload_to='resumes/%Y/%m/',blank=True,null=True,validators=[FileExtensionValidator(['pdf','doc','docx'])])
 def __str__(self):return self.user.username
class Job(models.Model):
 TYPE_CHOICES=[('Full-time','Full-time'),('Part-time','Part-time'),('Internship','Internship'),('Contract','Contract'),('Remote','Remote')]
 title=models.CharField(max_length=150)
 company=models.CharField(max_length=150)
 location=models.CharField(max_length=150)
 job_type=models.CharField(max_length=20,choices=TYPE_CHOICES,default='Full-time')
 salary=models.CharField(max_length=100,blank=True)
 description=models.TextField()
 requirements=models.TextField(blank=True)
 active=models.BooleanField(default=True)
 created_at=models.DateTimeField(auto_now_add=True)
 def __str__(self):return f'{self.title} - {self.company}'
class JobApplication(models.Model):
 STATUS_CHOICES=[('Applied','Applied'),('Under Review','Under Review'),('Shortlisted','Shortlisted'),('Interview','Interview'),('Selected','Selected'),('Rejected','Rejected')]
 seeker=models.ForeignKey(User,on_delete=models.CASCADE,related_name='job_applications')
 job=models.ForeignKey(Job,on_delete=models.CASCADE,related_name='applications')
 status=models.CharField(max_length=20,choices=STATUS_CHOICES,default='Applied')
 cover_letter=models.TextField(blank=True)
 applied_at=models.DateTimeField(auto_now_add=True)
 class Meta:
  constraints=[models.UniqueConstraint(fields=['seeker','job'],name='unique_job_application')]
  ordering=['-applied_at']
 def __str__(self):return f'{self.seeker.username}: {self.job.title}'
