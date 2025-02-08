from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('frontend.urls', namespace='frontend')),
    path('account/', include('account.urls', namespace='account')),
    path('account/transaction/', include('transaction.urls', namespace='transaction')),
    path('account/customer/', include('customer.urls', namespace='customer')),
]
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# urlpatterns += staticfiles_urlpatterns()