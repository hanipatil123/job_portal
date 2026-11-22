from django.db import models

class JobCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Employer(models.Model):

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    company_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.company_name

class JobPosting(models.Model):
    JOB_STATUS = [
        ('active', 'Active'),
        ('closed', 'Closed'),
    ]

    title = models.CharField(max_length=200)

    employer = models.ForeignKey(
        Employer,
        on_delete=models.CASCADE,
        related_name='job_postings'
    )

    category = models.ForeignKey(
        JobCategory,
        on_delete=models.PROTECT,
        related_name='job_postings'
    )

    location = models.CharField(max_length=150)
    salary = models.CharField(max_length=100, blank=True)
    description = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=JOB_STATUS,
        default='active'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
