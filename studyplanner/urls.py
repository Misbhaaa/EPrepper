from django.contrib import admin
from django.urls import path, include
from accounts.views import home,delete_account

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),  # 👈 This handles "/"
    path('', include('accounts.urls')),
    path('', include('subjects.urls')),
]