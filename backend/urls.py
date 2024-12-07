

from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

chema_view = get_schema_view(
   openapi.Info(
      title="E-commerce Backend APIs",
      default_version='v1',
      description="This is the API documentation for Desphixs LMS project APIs",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="destiny@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [ 
    path('swagger<format>/', get_schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('', get_schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', get_schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('admin/', admin.site.urls),

    path("api/v1/",include("api.urls"))
]

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_URL)
urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_URL)


