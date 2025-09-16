from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('candidate/dashboard/', views.candidate_dashboard, name='candidate_dashboard'),
    path('employer/dashboard/', views.employer_dashboard, name='employer_dashboard'),
    path('post/', views.post_job, name='post_job'),
    path('<int:job_id>/', views.job_detail, name='job_detail'),
    path('<int:job_id>/apply/', views.apply_job, name='apply_job'),
    path('<int:job_id>/applicants/', views.view_applicants, name='view_applicants'),
]
