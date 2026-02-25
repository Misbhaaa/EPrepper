from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import models
from datetime import date

from .models import Subject, Topic
from django.views.decorators.http import require_POST

@login_required
@require_POST
def delete_subject(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id, user=request.user)
    subject.delete()
    return redirect('dashboard')

@login_required
@require_POST
def delete_topic(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id, subject__user=request.user)
    subject_id = topic.subject.id
    topic.delete()
    return redirect('subject_detail', subject_id=subject_id)

@login_required
def subject_detail(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id, user=request.user)

    # Add topic
    if request.method == "POST" and "add_topic" in request.POST:
        name = request.POST.get('name')
        estimated_hours = request.POST.get('estimated_hours')

        if name and estimated_hours:
            Topic.objects.create(
                subject=subject,
                name=name,
                estimated_hours=estimated_hours
            )
        return redirect('subject_detail', subject_id=subject.id)

    # Mark complete
    if request.method == "POST" and "complete_topic" in request.POST:
        topic_id = request.POST.get('topic_id')
        topic = get_object_or_404(Topic, id=topic_id, subject=subject)
        topic.completed = True
        topic.save()
        return redirect('subject_detail', subject_id=subject.id)

    topics = Topic.objects.filter(subject=subject)

    total_topics = topics.count()
    completed_topics = topics.filter(completed=True).count()

    progress = int((completed_topics / total_topics) * 100) if total_topics > 0 else 0
    productivity_score = progress  # same calculation

    # -------- CALCULATE DAYS LEFT FIRST --------
    today = date.today()
    days_left = (subject.exam_date - today).days

    # -------- REQUIRED HOURS CALCULATION --------
    total_required_hours = topics.aggregate(
        total=models.Sum('estimated_hours')
    )['total'] or 0

    available_hours = subject.study_hours_per_day * max(days_left, 0)

    required_daily_hours = (
        round(total_required_hours / days_left, 2)
        if days_left > 0 else total_required_hours
    )

    status = "Not enough time ⚠️" if available_hours < total_required_hours else "On Track ✅"

    # -------- URGENCY CHECK (NOW SAFE) --------
    if days_left <= 3 and days_left > 0:
        urgency = "High 🚨"
    elif days_left <= 7 and days_left > 0:
        urgency = "Medium ⚠️"
    elif days_left <= 0:
        urgency = "Exam Passed ❌"
    else:
        urgency = "Low ✅"

    # -------- ADVANCED DAILY PLAN --------
    daily_plan = []
    incomplete_topics = topics.filter(completed=False)

    if days_left > 0 and incomplete_topics.exists():
        total_pending_hours = sum(t.estimated_hours for t in incomplete_topics)
        hours_per_day = round(total_pending_hours / days_left, 2)

        current_day = 1
        accumulated_hours = 0
        day_topics = []

        for topic in incomplete_topics:
            accumulated_hours += topic.estimated_hours
            day_topics.append(topic.name)

            if accumulated_hours >= hours_per_day:
                daily_plan.append({
                    "day": current_day,
                    "topics": day_topics,
                    "total_hours": accumulated_hours
                })
                current_day += 1
                accumulated_hours = 0
                day_topics = []

        if day_topics:
            daily_plan.append({
                "day": current_day,
                "topics": day_topics,
                "total_hours": accumulated_hours
            })

    return render(request, 'subject_detail.html', {
        'subject': subject,
        'topics': topics,
        'progress': progress,
        'days_left': days_left,
        'total_required_hours': total_required_hours,
        'available_hours': available_hours,
        'required_daily_hours': required_daily_hours,
        'status': status,
        'daily_plan': daily_plan,
        'productivity_score': productivity_score,
        'urgency': urgency
    })
@login_required
def add_subject(request):
    if request.method == "POST":
        name = request.POST['name']
        exam_date = request.POST['exam_date']
        study_hours = request.POST['study_hours']
        difficulty = request.POST['difficulty']

        Subject.objects.create(
            user=request.user,
            name=name,
            exam_date=exam_date,
            study_hours_per_day=study_hours,
            difficulty=difficulty
        )

        return redirect('dashboard')

    return render(request, 'add_subject.html')