"""RepickClone URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.flatpages import views as flat_views

from core.views import AjaxSearchView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^pages/', include('django.contrib.flatpages.urls')),
    url(r'^about/$', flat_views.flatpage, {'url': '/about/'}, name='about'),
    url(r'^terms/$', flat_views.flatpage, {'url': '/terms/'}, name='terms'),

    url(r'^froala_editor/', include('froala_editor.urls')),

    url(r'^', include('core.urls', namespace='core')),
    url(r'^catalogue/', include('catalogue.urls', namespace='catalogue')),
    url(r'^featured/', include('featured.urls', namespace='featured')),
    url(r'^likelist/', include('likelist.urls', namespace='likelist')),
    url(r'^search/', AjaxSearchView.as_view(), name='haystack_search')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
