from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages

from .models import Job, Application, CandidateProfile, EmployerProfile, UserProfile
from .forms import SignUpForm, CandidateProfileForm, EmployerProfileForm, JobForm

def home(request):
    # Search & filters
    q = request.GET.get('q', '')
    location = request.GET.get('location', '')
    min_salary = request.GET.get('min_salary', '')

    jobs = Job.objects.all().order_by('-posted_on')
    if q:
        jobs = jobs.filter(Q(title__icontains=q) | Q(description__icontains=q))
    if location:
        jobs = jobs.filter(location__icontains=location)
    if min_salary:
        try:
            ms = int(min_salary)
            jobs = jobs.filter(salary__gte=ms)
        except ValueError:
            pass

    return render(request, 'home.html', {'jobs': jobs, 'q': q, 'location': location, 'min_salary': min_salary})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            role = form.cleaned_data['role']

            # Create a UserProfile for role
            UserProfile.objects.create(user=user, role=role)

            if role == 'candidate':
                CandidateProfile.objects.create(user=user)
            else:
                EmployerProfile.objects.create(user=user, company_name=user.username)

            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def candidate_dashboard(request):
    # Ensure candidate
    if not hasattr(request.user, 'profile') or request.user.profile.role != 'candidate':
        messages.error(request, 'Only candidates can access this page.')
        return redirect('home')

    profile = request.user.candidate_profile
    if request.method == 'POST':
        form = CandidateProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated.')
            return redirect('candidate_dashboard')
    else:
        form = CandidateProfileForm(instance=profile)

    apps = profile.applications.select_related('job').order_by('-applied_on')
    return render(request, 'candidate/dashboard.html', {'form': form, 'applications': apps})

@login_required
def employer_dashboard(request):
    # Ensure employer
    if not hasattr(request.user, 'profile') or request.user.profile.role != 'employer':
        messages.error(request, 'Only employers can access this page.')
        return redirect('home')

    profile = request.user.employer_profile
    jobs = profile.jobs.all().order_by('-posted_on')
    return render(request, 'employer/dashboard.html', {'jobs': jobs})

@login_required
def post_job(request):
    if not hasattr(request.user, 'profile') or request.user.profile.role != 'employer':
        messages.error(request, 'Only employers can post jobs.')
        return redirect('home')

    profile = request.user.employer_profile
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.employer = profile
            job.save()
            messages.success(request, 'Job posted successfully!')
            return redirect('employer_dashboard')
    else:
        form = JobForm()
    return render(request, 'jobs/post_job.html', {'form': form})

def job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    return render(request, 'jobs/job_detail.html', {'job': job})

@login_required
def apply_job(request, job_id):
    if not hasattr(request.user, 'profile') or request.user.profile.role != 'candidate':
        messages.error(request, 'You must be a candidate to apply.')
        return redirect('home')

    job = get_object_or_404(Job, id=job_id)
    candidate = request.user.candidate_profile

    # Prevent duplicate applications
    if job.applications.filter(candidate=candidate).exists():
        messages.info(request, 'You have already applied for this job.')
        return redirect('job_detail', job_id=job.id)

    Application.objects.create(job=job, candidate=candidate)
    messages.success(request, 'Applied successfully!')
    return redirect('candidate_dashboard')

@login_required
def view_applicants(request, job_id):
    if not hasattr(request.user, 'profile') or request.user.profile.role != 'employer':
        messages.error(request, 'Only employers can view applicants.')
        return redirect('home')

    job = get_object_or_404(Job, id=job_id, employer=request.user.employer_profile)
    apps = job.applications.select_related('candidate__user')
    return render(request, 'jobs/applicants.html', {'job': job, 'applications': apps})
