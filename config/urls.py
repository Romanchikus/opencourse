"""opencourse URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.views.i18n import JavaScriptCatalog
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from opencourse.profiles.views import ProfileView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("courses/", include("opencourse.courses.urls", namespace="courses")),
    path("accounts/", include("allauth.urls")),
    path("accounts/profile/", ProfileView.as_view()),
    path("profiles/", include("opencourse.profiles.urls", namespace="profiles")),
    path("jsi18n/", JavaScriptCatalog.as_view(), name="javascript-catalog"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [path("__debug__/", include(debug_toolbar.urls)),] + urlpatterns
