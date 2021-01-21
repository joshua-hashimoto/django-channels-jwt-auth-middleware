from django.contrib import admin
from django.urls import path, include


def api_url(base_url=''):
    api_base_url = 'api/v1'
    if not base_url:
        return api_base_url + '/'
    return f'{api_base_url}/{base_url}/'


urlpatterns = [
    path('admin/', admin.site.urls),
    path(api_url('auth'), include('dj_rest_auth.urls')),
    path(api_url('auth/register'), include('dj_rest_auth.registration.urls')),
]
