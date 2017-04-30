from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import reverse_lazy
from django.views.generic import RedirectView

urlpatterns = [
	url(r'^admin/', include(admin.site.urls)),
	url(r'^$', RedirectView.as_view(url=reverse_lazy('admin:index'))),
]

# Makes media files work on dev server
if settings.DEBUG:
	import debug_toolbar
	urlpatterns += [
		url(r'^__debug__/', include(debug_toolbar.urls)),
	] + \
		static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + \
		static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
