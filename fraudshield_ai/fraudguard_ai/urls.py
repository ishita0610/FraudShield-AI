from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.about.urls')),
    path('accounts/', include('apps.accounts.urls')),
    path('dashboard/', include('apps.dashboard.urls')),
    path('transactions/', include('apps.transactions.urls')),
]
