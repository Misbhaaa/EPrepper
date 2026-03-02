from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from subjects.models import Subject, Topic
from django.views.decorators.http import require_POST
from django.contrib.auth import logout


from django.utils import timezone
from datetime import datetime, timedelta
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
import random
from django.conf import settings

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

            # 🔹 Check if OTP verified within last 1 hour
            otp_time = request.session.get('otp_verified_time')

            if otp_time:
                otp_time = datetime.fromisoformat(otp_time)

                if timezone.now() - otp_time < timedelta(hours=1):
                    login(request, user)
                    return redirect('dashboard')

            # 🔹 Generate OTP
            otp = random.randint(100000, 999999)

            request.session['otp'] = otp
            request.session['temp_user'] = user.username
            request.session['otp_expiry'] = (
                timezone.now() + timedelta(minutes=5)
            ).isoformat()

            subject = "Your One-Time Password (OTP) for Verification"

            html_content = f"""
            <html>
            <body style="font-family: Arial, sans-serif; background-color: #f4f6fa; padding: 20px;">
                <div style="max-width: 600px; margin: auto; background: #ffffff; padding: 30px; border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.1);">
                    
                    <h2 style="color: #2c3e50;">Hello {user.username},</h2>
                    
                    <p>Thank you for using <strong>EPrepper</strong>.</p>

                    <p>Your One-Time Password (OTP) for verification is:</p>

                    <div style="text-align:center; margin:20px 0;">
                        <span style="font-size:28px; font-weight:bold; letter-spacing:4px; color:#0d6efd;">
                            {otp}
                        </span>
                    </div>

                    <p>This OTP is valid for <strong>5 minutes</strong>. Please do not share it.</p>

                    <hr>

                    <p>If you did not request this OTP, please ignore this email.</p>

                    <p>
                        Best regards,<br>
                        <strong>EPrepper Team</strong>
                    </p>
                </div>
            </body>
            </html>
            """

            text_content = strip_tags(html_content)

            email = EmailMultiAlternatives(
                subject,
                text_content,
                settings.EMAIL_HOST_USER,   # ✅ CORRECT
                [user.email],
            )

            email.attach_alternative(html_content, "text/html")
            email.send()

            return redirect('verify_otp')

        else:
            messages.error(request, "Invalid credentials")

    return render(request, 'login.html')


def verify_otp(request):
    if request.method == "POST":
        entered_otp = request.POST['otp']
        session_otp = request.session.get('otp')
        expiry_time = request.session.get('otp_expiry')

        if not session_otp or not expiry_time:
            messages.error(request, "Session expired. Please login again.")
            return redirect('login')

        expiry_time = datetime.fromisoformat(expiry_time)

        if timezone.now() > expiry_time:
            messages.error(request, "OTP expired. Please login again.")
            return redirect('login')

        if str(entered_otp) == str(session_otp):
            username = request.session.get('temp_user')
            user = User.objects.get(username=username)

            login(request, user)

            request.session['otp_verified_time'] = timezone.now().isoformat()

            request.session.pop('otp', None)
            request.session.pop('temp_user', None)
            request.session.pop('otp_expiry', None)

            return redirect('dashboard')

        else:
            messages.error(request, "Invalid OTP")

    return render(request, 'verify_otp.html')

def user_logout(request):
    logout(request)
    return redirect('login')