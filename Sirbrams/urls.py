from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path(
        "manifest.json",
        TemplateView.as_view(
            template_name="manifest.json",
            content_type="application/manifest+json",
        ),
        name="manifest.json",
    ),
    path(
        "sw.js",
        TemplateView.as_view(
            template_name="sw.js",
            content_type="application/javascript",
        ),
        name="sw.js",
    ),
    path("", include("TechApp.urls")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
