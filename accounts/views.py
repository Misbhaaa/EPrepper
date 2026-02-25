from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from subjects.models import Subject, Topic
from django.views.decorators.http import require_POST
from django.contrib.auth import logout

@login_required
@require_POST
def delete_account(request):
    user = request.user
    logout(request)
    user.delete()
    return redirect('login')

def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return redirect('login')


@login_required
def dashboard(request):
    subjects = Subject.objects.filter(user=request.user)

    subject_data = []

    total_completed = 0
    total_pending = 0

    for subject in subjects:
        topics = Topic.objects.filter(subject=subject)
        total = topics.count()
        completed = topics.filter(completed=True).count()
        pending = total - completed

        total_completed += completed
        total_pending += pending

        if total > 0:
            progress = int((completed / total) * 100)
        else:
            progress = 0

        subject_data.append({
            'subject': subject,
            'progress': progress,
            'total': total,
            'completed': completed
        })

    # 🔥 Data for Bar Chart
    subject_names = [item['subject'].name for item in subject_data]
    subject_progress = [item['progress'] for item in subject_data]

    return render(request, 'dashboard.html', {
        'subject_data': subject_data,
        'total_completed': total_completed,
        'total_pending': total_pending,
        'subject_names': subject_names,
        'subject_progress': subject_progress
    })


def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('register')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        user.save()
        messages.success(request, "Account created successfully")
        return redirect('login')

    return render(request, 'register.html')


def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid credentials")

    return render(request, 'login.html')


def user_logout(request):
    logout(request)
    return redirect('login')