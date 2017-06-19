from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import reverse_lazy
from django.views.generic import RedirectView
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Hubs API')

urlpatterns = [
	url(r'^admin/', include(admin.site.urls)),
	url(r'^core/', include('apps.core.urls', namespace='core')),
	url(r'^school/', include('apps.school.urls', namespace='school')),
	url(r'^absence/', include('apps.absence.urls', namespace='absence')),
	url(r'^notifications/', include('apps.notifications.urls', namespace='notifications')),
	url(r'^stats/', include('apps.stats.urls', namespace='stats')),
	url(r'^$', RedirectView.as_view(url=reverse_lazy('admin:index'))),
	url(r'^schema/$', schema_view),
]

# Makes media files work on dev server
if settings.DEBUG:
	import debug_toolbar
	urlpatterns += [
		url(r'^__debug__/', include(debug_toolbar.urls)),
	] + \
		static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + \
		static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
