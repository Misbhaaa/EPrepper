from django.urls import path
from . import views

urlpatterns = [
    path('add-subject/', views.add_subject, name='add_subject'),
    path('subject/<int:subject_id>/', views.subject_detail, name='subject_detail'),
    path('delete-subject/<int:subject_id>/', views.delete_subject, name='delete_subject'),
    path('delete-topic/<int:topic_id>/', views.delete_topic, name='delete_topic'),
]