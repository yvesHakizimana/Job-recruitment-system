from django.contrib import admin

from accounts.models import User, JobPost, Application


# Register admin models
@admin.register(JobPost)
class JobPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'employer', 'employment_type', 'location', 'posted_at', 'application_deadline')
    list_filter = ('employment_type', 'location', 'posted_at', 'application_deadline')
    search_fields = ('title', 'description', 'employer__username')


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('candidate', 'job_post', 'status', 'applied_at')
    list_filter = ('status', 'applied_at')
    search_fields = ('candidate__username', 'job_post__title')



