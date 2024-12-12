import datetime

from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.db.models import Count
from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import TemplateView, UpdateView, CreateView, ListView, DetailView

from accounts.forms import EmployeeSignUpForm, CandidateSignUpForm, JobPostForm, ApplicationStatusForm, \
    JobPostSearchForm, ApplicationForm, EmployerProfileUpdateForm, CandidateProfileUpdateForm
from accounts.models import JobPost, Application, EmployerProfile, CandidateProfile


# Create your views here.
class EmployeeSignUpView(View):
    def get(self, request):
        form = EmployeeSignUpForm()
        return render(request, 'accounts/employer_signup.html', {'form': form})

    def post(self, request):
        form = EmployeeSignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful. Welcome Employer!')
            return redirect('employer_dashboard')
        return render(request, 'accounts/employer_signup.html', {'form': form})


class CandidateSignUpView(View):
    def get(self, request):
        form = CandidateSignUpForm()
        return render(request, 'accounts/candidate_signup.html', {'form': form})

    def post(self, request):
        form = CandidateSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful. Welcome Candidate!')
            return redirect('candidate_dashboard')
        return render(request, 'accounts/candidate_signup.html', {'form': form})


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'

    def get_success_url(self):
        user = self.request.user
        if user.is_authenticated:
            if user.is_employer():
                return reverse_lazy('employer_dashboard')
            elif user.is_candidate():
                return reverse_lazy('candidate_dashboard')
        return super().get_success_url()


def logout_view(request):
    logout(request)
    return redirect('login')


class EmployerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_employer()

    def handle_no_permission(self):
        messages.error(self.request, 'You do not have permission to perform this action.')
        return redirect('login')


class CandidateRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_candidate()

    def handle_no_permission(self):
        messages.error(self.request, 'You do not have permission to perform this action.')
        return redirect('login')


class EmployeeDashboardView(LoginRequiredMixin, EmployerRequiredMixin, TemplateView):
    template_name = 'accounts/dashboards/employer_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        job_posts = JobPost.objects.filter(employer=self.request.user).annotate(
            application_count=Count('applications')
        )
        total_applications = Application.objects.filter(job_post__employer=self.request.user).count()
        applications_by_status = Application.objects.filter(job_post__employer=self.request.user).values(
            'status').annotate(count=Count('status'))
        context['job_posts'] = job_posts
        context['total_applications'] = total_applications
        context['applications_by_status'] = applications_by_status
        return context


class CandidateDashboardView(LoginRequiredMixin, CandidateRequiredMixin, TemplateView):
    template_name = 'accounts/dashboards/candidate_dashboard.html'


# Create Job Post by Employer
class CreateJobPostView(LoginRequiredMixin, EmployerRequiredMixin, CreateView):
    model = JobPost
    form_class = JobPostForm
    template_name = 'accounts/job/create_job_post.html'
    success_url = reverse_lazy('employer_dashboard')

    def form_valid(self, form):
        form.instance.employer = self.request.user
        messages.success(self.request, 'Job post successfully created.')
        return super().form_valid(form)


# View Job Posts created by Employer
class JobPostView(LoginRequiredMixin, EmployerRequiredMixin, ListView):
    model = JobPost
    template_name = 'accounts/job/job_post_list.html'
    context_object_name = 'job_posts'

    def get_queryset(self):
        return JobPost.objects.filter(employer=self.request.user).order_by('-posted_at')


# Get the details of a specific Job Post
class JobPostDetailView(LoginRequiredMixin, EmployerRequiredMixin, DetailView):
    model = JobPost
    template_name = 'accounts/job/job_post_details.html'
    context_object_name = 'job_post'

    def get_queryset(self):
        return JobPost.objects.filter(employer=self.request.user).order_by('-posted_at')


# Get all applications of a specific job Post.
class ApplicationListView(LoginRequiredMixin, EmployerRequiredMixin, ListView):
    model = Application
    template_name = 'accounts/application/application_list.html'
    context_object_name = 'applications'

    def get_queryset(self):
        job_post = get_object_or_404(JobPost, pk=self.kwargs['pk'], employer=self.request.user)
        return Application.objects.filter(job_post=job_post).order_by('-applied_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['job_post'] = get_object_or_404(JobPost, pk=self.kwargs['pk'], employer=self.request.user)
        return context


# Review and update the application status of the candidate
class UpdateApplicationStatusView(LoginRequiredMixin, EmployerRequiredMixin, UpdateView):
    model = Application
    form_class = ApplicationStatusForm
    template_name = 'accounts/application/update_application_status.html'

    def get_success_url(self):
        job_post_pk = self.object.job_post.pk
        return reverse('applications_list', kwargs={'pk': job_post_pk})

    def get_queryset(self):
        return Application.objects.filter(job_post__employer=self.request.user).order_by('-applied_at')

    def form_valid(self, form):
        messages.success(self.request, 'Application status updated.')
        return super().form_valid(form)


# Lists the Available jobs.
class JobPostListView(ListView):
    model = JobPost
    template_name = 'accounts/candidate/job_post_list.html'
    context_object_name = 'job_posts'
    paginate_by = 10

    def get_queryset(self):
        today = datetime.date.today()
        queryset = JobPost.objects.filter(application_deadline__gte=today)
        form = self.get_search_form()
        if form.is_valid():
            title = form.cleaned_data['title']
            location = form.cleaned_data['location']
            min_salary = form.cleaned_data['min_salary']
            max_salary = form.cleaned_data['max_salary']

            if title:
                queryset = queryset.filter(title__icontains=title)
            if location:
                queryset = queryset.filter(location__icontains=location)
            if min_salary:
                queryset = queryset.filter(salary__gte=min_salary)
            if max_salary:
                queryset = queryset.filter(salary__lte=max_salary)
        return queryset.order_by('-posted_at')

    def get_search_form(self):
        if self.request.method == 'POST':
            return JobPostSearchForm(self.request.POST)
        return JobPostSearchForm()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = self.get_search_form()
        return context


# Get details of the JobPost.
class JobPostDetailsView(DetailView):
    model = JobPost
    template_name = 'accounts/candidate/job_post_details.html'
    context_object_name = 'job_post'


class ApplyToJobView(LoginRequiredMixin, CandidateRequiredMixin, CreateView):
    model = Application
    form_class = ApplicationForm
    template_name = 'accounts/candidate/apply_job.html'
    # redirect to candidate Applications
    success_url = reverse_lazy('candidate_applications')

    def dispatch(self, request, *args, **kwargs):
        today = datetime.date.today()
        self.job_post = get_object_or_404(JobPost, pk=kwargs['pk'], application_deadline__gte=today)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # Prevent duplicate applications
        if Application.objects.filter(job_post=self.job_post, candidate=self.request.user).exists():
            form.add_error(None, "You have already applied to this job.")
            return self.form_invalid(form)

        form.instance.candidate = self.request.user
        form.instance.job_post = self.job_post
        messages.success(self.request, 'Your application has been submitted successfully.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['job_post'] = self.job_post
        return context


class CandidateApplicationsListView(LoginRequiredMixin, CandidateRequiredMixin, ListView):
    model = Application
    template_name = 'accounts/candidate/candidate_applications.html'
    context_object_name = 'applications'
    paginate_by = 10  # Number of applications per page

    def get_queryset(self):
        return Application.objects.filter(candidate=self.request.user).order_by('-applied_at')


class EmployerProfileUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = EmployerProfile
    form_class = EmployerProfileUpdateForm
    template_name = 'accounts/profile/employer_profile_update.html'
    success_url = reverse_lazy('employer_dashboard')

    def get_object(self, queryset=None):
        return self.request.user.employerprofile

    def test_func(self):
        return self.request.user.role == 'employer'


class CandidateProfileUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = CandidateProfile
    form_class = CandidateProfileUpdateForm
    template_name = 'accounts/profile/candidate_profile_update.html'
    success_url = reverse_lazy('candidate_dashboard')

    def get_object(self, queryset=None):
        return self.request.user.candidateprofile

    def test_func(self):
        return self.request.user.role == 'candidate'


class HomeView(TemplateView):
    template_name = 'home.html'
