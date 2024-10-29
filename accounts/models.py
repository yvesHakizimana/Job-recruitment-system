from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


# Create your models here.
class User(AbstractUser):
    ROLE_CHOICES = (
        ('employer', 'Employer'),
        ('candidate', 'Candidate'),
    )

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='employer')

    def is_employer(self):
        return self.role == 'employer'

    def is_candidate(self):
        return self.role == 'candidate'


class EmployerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=120)
    company_description = models.TextField()
    company_logo = models.ImageField(upload_to='company_logo/', null=True, blank=True)

    def __str__(self):
        return self.user.username


class CandidateProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    resume = models.FileField(upload_to='resume/', null=True, blank=True)
    skills = models.TextField(null=True, blank=True)
    experience = models.TextField(null=True, blank=True)
    education = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.user.username


class JobPost(models.Model):
    EMPLOYMENT_TYPE_CHOICES = (
        ('full_time', 'Full-Time'),
        ('part_time', 'Part-Time'),
        ('contract', 'Contract'),
        ('internship', 'Internship'),
    )

    employer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='job_posts')
    title = models.CharField(max_length=255)
    description = models.TextField()
    employment_type = models.CharField(max_length=10, choices=EMPLOYMENT_TYPE_CHOICES)
    location = models.CharField(max_length=255)
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    posted_at = models.DateTimeField(auto_now_add=True)
    application_deadline = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.title} at {self.employer.username}"


class Application(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('interviewed', 'Interviewed'),
        ('hired', 'Hired'),
        ('rejected', 'Rejected'),
    )

    job_post = models.ForeignKey(JobPost, on_delete=models.CASCADE, related_name='applications')
    candidate = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='applications')
    cover_letter = models.TextField(null=True, blank=True)
    applied_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"Application by {self.candidate.username} for {self.job_post.title}"

