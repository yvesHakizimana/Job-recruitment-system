# Job Recruitment System

## Overview
The **Job Recruitment System** is a web-based application built with Django, HTML, CSS, and MySQL. It facilitates seamless interaction between employers and candidates for job recruitment purposes. The system includes features for user registration, job postings, application management, and dashboards for both employers and candidates.

---

## Table of Contents
1. [Technologies Used](#technologies-used)
2. [Features](#features)
3. [Installation](#installation)
4. [Configuration](#configuration)
5. [Database Models](#database-models)
6. [User Roles](#user-roles)
7. [Project Structure](#project-structure)
8. [Usage](#usage)
9. [Future Enhancements](#future-enhancements)

---

## Technologies Used
- **Backend**: Django 5.1.2 (Python web framework)
- **Frontend**: HTML, CSS (with Bootstrap 5 and Crispy Forms for enhanced UI/UX)
- **Database**: MySQL
- **Other Tools**: 
  - Decouple (for environment variable management)
  - Crispy Forms and Crispy Bootstrap 5 (for form rendering)

---

## Features
- **User Registration and Authentication**: Separate sign-up processes for Employers and Candidates.
- **Role-based Dashboard**: Distinct dashboards for Employers and Candidates.
- **Job Posting and Application**: Employers can create job posts, and Candidates can view and apply for jobs.
- **Application Management**: Employers can view applications for their job posts and update the status of candidates.
- **User Profiles**: Employers and Candidates can manage their profiles, including uploading resumes and company logos.
- **Secure Login and Logout**: Authentication system using Django’s `LoginView`.
- **File Uploads**: Upload resumes for candidates and company logos for employers.

---

## Installation
### Prerequisites
- Python 3.8+
- MySQL database
- pip (Python package installer)

### Steps
1. **Clone the repository**
   ```bash
   git clone https://github.com/your-repository-link/job-recruitment-system.git
   cd job-recruitment-system
   ```

2. **Create and activate a virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # For Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the MySQL database**
   - Create a new MySQL database and update the `.env` file with the following:
     ```env
     DB_NAME=your_database_name
     DB_USER=your_database_user
     DB_PASSWORD=your_database_password
     DB_HOST=your_database_host
     DB_PORT=your_database_port
     ```

5. **Run database migrations**
   ```bash
   python manage.py migrate
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

Access the application at: `http://127.0.0.1:8000/`

---

## Configuration
### Environment Variables
The project uses `python-decouple` to manage environment variables. Create a `.env` file in the root directory with the following keys:
```env
SECRET_KEY=your_secret_key
DEBUG=True  # Set to False in production
DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_HOST=your_database_host
DB_PORT=your_database_port
```

---

## Database Models
1. **User** (AbstractUser):
   - `role`: Determines if the user is an **Employer** or **Candidate**.
   
2. **EmployerProfile**:
   - One-to-one relationship with the User model.
   - Stores company details, including logo and description.

3. **CandidateProfile**:
   - One-to-one relationship with the User model.
   - Stores candidate details, including resume, skills, experience, and education.

4. **JobPost**:
   - Represents a job created by an employer.
   - Tracks information such as title, description, employment type, location, and salary.

5. **Application**:
   - Tracks applications made by candidates to job posts.
   - Each application tracks candidate details, the associated job post, and the status of the application.

---

## User Roles
1. **Employer**
   - Can create, view, and manage job posts.
   - Can view applications for their job posts and update their status.
   - Can update their profile and company information.

2. **Candidate**
   - Can browse and search for job posts.
   - Can view job post details and submit applications with a cover letter.
   - Can track the status of applications through their dashboard.
   - Can update their profile, including skills, education, and resume.

---

## Project Structure
```
job_recruitment_system/
|-- accounts/
|   |-- migrations/
|   |-- templates/accounts/
|   |-- __init__.py
|   |-- admin.py
|   |-- apps.py
|   |-- models.py
|   |-- forms.py
|   |-- views.py
|-- job_recruitment_system/
|   |-- __init__.py
|   |-- settings.py
|   |-- urls.py
|   |-- wsgi.py
|-- templates/
|   |-- home.html
|-- static/
|-- media/
|-- manage.py
```

---

## Usage
### Employer
1. **Sign Up** as an Employer.
2. Access the **Employer Dashboard**.
3. **Create Job Posts** and view the list of job posts.
4. **Review Applications** for posted jobs and update their status.
5. **Update Profile** information, including the company logo.

### Candidate
1. **Sign Up** as a Candidate.
2. Access the **Candidate Dashboard**.
3. **Browse Available Jobs** and search using filters.
4. **Apply for Jobs** and track application status.
5. **Update Profile** with skills, experience, and education.

---

## Future Enhancements
- **Notifications**: Email or in-app notifications for candidates and employers.
- **Advanced Search**: Enable filtering by location, salary range, and employment type.
- **Admin Dashboard**: Advanced admin functionalities to manage users, jobs, and applications.
- **Resume Parsing**: Extract relevant information automatically from uploaded resumes.
- **Analytics**: Data visualization for job applications and status.

---

## License
This project is licensed under the MIT License.

## Contact
For any issues, feature requests, or contributions, please contact [Your Name] at [your-email@example.com].
