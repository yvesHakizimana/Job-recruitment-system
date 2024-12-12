from django.urls import path

from accounts.views import EmployeeSignUpView, CandidateSignUpView, CustomLoginView, \
    EmployeeDashboardView, CandidateDashboardView, logout_view, JobPostView, CreateJobPostView, JobPostDetailView, \
    ApplicationListView, UpdateApplicationStatusView, JobPostListView, JobPostDetailsView, ApplyToJobView, \
    CandidateApplicationsListView, EmployerProfileUpdateView

urlpatterns = [
    path('signup/employer/', EmployeeSignUpView.as_view(), name='employer_signup'),
    path('signup/candidate/', CandidateSignUpView.as_view(), name='candidate_signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),

    # Employer Dashboard
    path('dashboard/employer/', EmployeeDashboardView.as_view(), name='employer_dashboard'),

    # Candidate Dashboard
    path('dashboard/candidate/', CandidateDashboardView.as_view(), name='candidate_dashboard'),


    # Employer Job Postings
    path('dashboard/employer/job-posts', JobPostView.as_view(), name='job_posts_list'),
    path('dashboard/employer/job_posts/create', CreateJobPostView.as_view(), name='create_job_post'),
    path('dashboard/employer/job_posts/<int:pk>/', JobPostDetailView.as_view(), name='job_post_detail'),

    # Applications
    path('dashboard/employer/job-posts/<int:pk>/applications', ApplicationListView.as_view(), name='applications_list'),
    path('dashboard/employer/applications/<int:pk>/update', UpdateApplicationStatusView.as_view(), name='update_application_status'),

    # Candidate Module Urls
    path('jobs/', JobPostListView.as_view(), name='jobs_list'),
    path('jobs/<int:pk>/', JobPostDetailsView.as_view(), name='job_post_detail'),
    path('jobs/<int:pk>/apply', ApplyToJobView.as_view(), name='apply_to_job'),
    path('applications/', CandidateApplicationsListView.as_view(), name='candidate_applications'),

    # Update forms
    path('profile/update/employer', EmployerProfileUpdateView.as_view(), name='employer_profile_update'),
    path('profile/update/candidate', CandidateApplicationsListView.as_view(), name='candidate_profile_update'),
]
