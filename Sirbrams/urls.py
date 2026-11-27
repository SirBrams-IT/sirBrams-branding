from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, re_path, include
from django.views.static import serve
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
    # Portfolio uploads. WhiteNoise only serves static files, so media is
    # served here; it works with DEBUG on or off.
    re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
    path("", include("TechApp.urls")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
