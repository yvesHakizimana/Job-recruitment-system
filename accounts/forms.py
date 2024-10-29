# accounts/forms.py

# accounts/forms.py
from .models import User, EmployerProfile, CandidateProfile, JobPost, Application

from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import User, EmployerProfile
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Row, Column
from django.contrib.auth.password_validation import validate_password


class EmployeeSignUpForm(UserCreationForm):
    company_name = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Company Name'
        })
    )
    company_description = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'Describe your company...',
            'rows': 4
        }),
        required=True
    )
    company_logo = forms.ImageField(
        required=False
    )

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'password1',
            'password2',
            'company_name',
            'company_description',
            'company_logo'
        )
        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder': 'Username'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Email'
            }),
            'password1': forms.PasswordInput(attrs={
                'placeholder': 'Password'
            }),
            'password2': forms.PasswordInput(attrs={
                'placeholder': 'Confirm Password'
            }),
        }
        help_texts = {
            'password1': 'Your password can’t be too similar to your other personal information.',
            'password2': 'Enter the same password as before, for verification.',
        }

    def __init__(self, *args, **kwargs):
        super(EmployeeSignUpForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('username', css_class='form-group col-md-6 mb-0'),
                Column('email', css_class='form-group col-md-6 mb-0'),
                css_class='row'
            ),
            Row(
                Column('password1', css_class='form-group col-md-6 mb-0'),
                Column('password2', css_class='form-group col-md-6 mb-0'),
                css_class='row'
            ),
            'company_name',
            'company_description',
            'company_logo',
            Submit('submit', 'Sign Up', css_class='btn btn-primary mt-3')
        )

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        validate_password(password1, self.instance)
        return password1

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'employer'
        if commit:
            user.save()
            EmployerProfile.objects.create(
                user=user,
                company_name=self.cleaned_data['company_name'],
                company_description=self.cleaned_data['company_description'],
                company_logo=self.cleaned_data.get('company_logo')
            )
        return user


class CandidateSignUpForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'placeholder': 'Email'
        })
    )
    resume = forms.FileField(
        required=False
    )
    skills = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'List your skills...',
            'rows': 3
        }),
        required=False
    )
    experience = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'Describe your experience...',
            'rows': 3
        }),
        required=False
    )
    education = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'Detail your education...',
            'rows': 3
        }),
        required=False
    )

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2',
            'resume',
            'skills',
            'experience',
            'education'
        ]
        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder': 'Username'
            }),
            'password1': forms.PasswordInput(attrs={
                'placeholder': 'Password'
            }),
            'password2': forms.PasswordInput(attrs={
                'placeholder': 'Confirm Password'
            }),
        }
        help_texts = {
            'password1': 'Your password can’t be too similar to your other personal information.',
            'password2': 'Enter the same password as before, for verification.',
        }

    def __init__(self, *args, **kwargs):
        super(CandidateSignUpForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('username', css_class='form-group col-md-6 mb-0'),
                Column('email', css_class='form-group col-md-6 mb-0'),
                css_class='row'
            ),
            Row(
                Column('password1', css_class='form-group col-md-6 mb-0'),
                Column('password2', css_class='form-group col-md-6 mb-0'),
                css_class='row'
            ),
            'resume',
            'skills',
            'experience',
            'education',
            Submit('submit', 'Sign Up', css_class='btn btn-primary mt-3')
        )

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        validate_password(password1, self.instance)
        return password1

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'candidate'
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            CandidateProfile.objects.create(
                user=user,
                resume=self.cleaned_data.get('resume'),
                skills=self.cleaned_data.get('skills'),
                experience=self.cleaned_data.get('experience'),
                education=self.cleaned_data.get('education')
            )
        return user


class JobPostForm(forms.ModelForm):
    class Meta:
        model = JobPost
        fields = [
            'title',
            'description',
            'employment_type',
            'location',
            'salary',
            'application_deadline'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Job Title'
            }),
            'description': forms.Textarea(attrs={
                'placeholder': 'Job Description',
                'rows': 5
            }),
            'employment_type': forms.Select(attrs={'class': 'form-select'}),
            'location': forms.TextInput(attrs={
                'placeholder': 'Location'
            }),
            'salary': forms.NumberInput(attrs={
                'placeholder': 'Salary'
            }),
            'application_deadline': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
        }

    def __init__(self, *args, **kwargs):
        super(JobPostForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'title',
            'description',
            'employment_type',
            'location',
            'salary',
            'application_deadline',
            Submit('submit', 'Post Job', css_class='btn btn-success mt-3')
        )


class ApplicationStatusForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['status']

    def __init__(self, *args, **kwargs):
        super(ApplicationStatusForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'status',
            Submit('submit', 'Update Status', css_class='btn btn-primary mt-3')
        )


class JobPostSearchForm(forms.Form):
    title = forms.CharField(
        required=False,
        label='Job Title'
    )
    location = forms.CharField(
        required=False,
        label='Location'
    )
    min_salary = forms.DecimalField(
        required=False,
        label='Minimum Salary',
        min_value=0
    )
    max_salary = forms.DecimalField(
        required=False,
        label='Maximum Salary',
        min_value=0
    )
    sort_by = forms.ChoiceField(
        required=False,
        label='Sort By',
        choices=[
            ('', 'Default'),
            ('employment_type_asc', 'Employment Type (A-Z)'),
            ('employment_type_desc', 'Employment Type (Z-A)'),
            # Add more sorting options if needed
        ]
    )

    def __init__(self, *args, **kwargs):
        super(JobPostSearchForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.layout = Layout(
            Row(
                Column('title', css_class='form-group col-md-3 mb-0'),
                Column('location', css_class='form-group col-md-3 mb-0'),
                Column('min_salary', css_class='form-group col-md-2 mb-0'),
                Column('max_salary', css_class='form-group col-md-2 mb-0'),
                Column('sort_by', css_class='form-group col-md-2 mb-0'),
                css_class='row'
            ),
            Row(
                Column(
                    Submit('submit', 'Search', css_class='btn btn-primary mt-3'),
                    css_class='d-flex justify-content-end'
                )
            )
        )

    def clean(self):
        cleaned_data = super().clean()
        min_salary = cleaned_data.get('min_salary')
        max_salary = cleaned_data.get('max_salary')

        if min_salary and max_salary and min_salary > max_salary:
            raise forms.ValidationError("Minimum salary cannot exceed maximum salary.")

        return cleaned_data


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['cover_letter']
        labels = {
            'cover_letter': 'Cover Letter (Optional)',
        }
        widgets = {
            'cover_letter': forms.Textarea(attrs={
                'placeholder': 'Write your cover letter here...',
                'rows': 5
            }),
        }

    def __init__(self, *args, **kwargs):
        super(ApplicationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'cover_letter',
            Submit('submit', 'Apply', css_class='btn btn-success mt-3')
        )


# Update Employer Profile
class EmployerProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = EmployerProfile
        fields = ['company_name', 'company_description', 'company_logo']
        widgets = {
            'company_description': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Describe your company...'
            }),
            'company_logo': forms.ClearableFileInput(),
        }

    def __init__(self, *args, **kwargs):
        super(EmployerProfileUpdateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('company_name', css_class='form-group col-md-6 mb-0'),
                Column('company_logo', css_class='form-group col-md-6 mb-0'),
                css_class='row'
            ),
            'company_description',
            Submit('submit', 'Update Profile', css_class='btn btn-primary mt-3')
        )


# Update Candidate Profile
class CandidateProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CandidateProfile
        fields = ['resume', 'skills', 'experience', 'education']
        widgets = {
            'skills': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'List your skills...'
            }),
            'experience': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Describe your experience...'
            }),
            'education': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Detail your education...'
            }),
            'resume': forms.ClearableFileInput(),
        }

    def __init__(self, *args, **kwargs):
        super(CandidateProfileUpdateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'resume',
            'skills',
            'experience',
            'education',
            Submit('submit', 'Update Profile', css_class='btn btn-primary mt-3')
        )
