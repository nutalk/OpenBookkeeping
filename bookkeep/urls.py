"""
URL configuration for bookkeep project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from accounts.views import details, book_check
from accounts.report_views import report, account_ana

page_urls = i18n_patterns(
    path("", details, name='details'),
    path('check/', book_check, name='check'),
    path('report/', report, name='report'),
    path('account_ana/', account_ana, name="account_ana")
)

urlpatterns = [
    path('', include('accounts.urls')),
    path('admin/', admin.site.urls),
]

urlpatterns += page_urls