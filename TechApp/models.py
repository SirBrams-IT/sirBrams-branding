import io
import os

from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.core.validators import FileExtensionValidator
from django.db import models
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver

class Contact(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    response = models.TextField(blank=True, null=True)
    is_replied = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"

class Payment(models.Model):
    order_id = models.CharField(max_length=255)
    payer_id = models.CharField(max_length=255)
    status = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payer_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.id} - {self.status}"


# ---------------------------------------------------------------------------
# Portfolio (managed from the admin panel)
# ---------------------------------------------------------------------------
MAX_UPLOAD_MB = 8
MAX_IMAGE_EDGE = 1600  # longest side, in pixels, after optimising


def validate_image_size(f):
    if f.size > MAX_UPLOAD_MB * 1024 * 1024:
        raise ValidationError(f"Image is too large. Please keep it under {MAX_UPLOAD_MB} MB.")


def optimise_image(uploaded):
    """Return a web-friendly WebP copy of an uploaded image.

    Keeps pages fast: phone photos and big exports are scaled to at most
    1600px and re-encoded. If the file is not a raster image Pillow can read,
    the original is returned untouched.
    """
    try:
        from PIL import Image, ImageOps

        uploaded.seek(0)
        img = ImageOps.exif_transpose(Image.open(uploaded))
        img.thumbnail((MAX_IMAGE_EDGE, MAX_IMAGE_EDGE))
        has_alpha = img.mode in ("RGBA", "LA", "P")
        img = img.convert("RGBA" if has_alpha else "RGB")
        buf = io.BytesIO()
        img.save(buf, format="WEBP", quality=84, method=6)
        stem = os.path.splitext(os.path.basename(uploaded.name))[0]
        return ContentFile(buf.getvalue(), name=f"{stem}.webp")
    except Exception:
        uploaded.seek(0)
        return uploaded


class PortfolioItem(models.Model):
    WEB = "web"
    DESIGN = "design"
    CATEGORY_CHOICES = [
        (WEB, "Website or system"),
        (DESIGN, "Graphic design"),
    ]

    title = models.CharField(max_length=120)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default=WEB)
    tag = models.CharField(
        "Industry or type", max_length=60, blank=True,
        help_text="Websites: the industry, e.g. Education. Designs: the kind of piece, e.g. Logo or Flyer.",
    )
    summary = models.TextField(
        "Description", max_length=600,
        help_text="Websites: a short summary of what it does. Designs: the client brief.",
    )
    notes = models.TextField(
        "Colour and branding notes", blank=True, max_length=600,
        help_text="Designs only. Shown beside the large preview.",
    )
    stack = models.CharField(
        "Built with", max_length=200, blank=True,
        help_text="Websites only. Separate with commas, e.g. Django, Bootstrap, M-Pesa.",
    )
    url = models.URLField(
        "Live site address", blank=True,
        help_text="Websites only. Leave empty if it is not live yet.",
    )
    image = models.ImageField(
        upload_to="portfolio/%Y/%m/", blank=True,
        validators=[
            FileExtensionValidator(["jpg", "jpeg", "png", "webp", "gif"]),
            validate_image_size,
        ],
        help_text="Screenshot (websites) or the finished design. JPG, PNG or WebP, up to 8 MB. "
                  "It is resized and compressed automatically.",
    )
    is_published = models.BooleanField(
        "Show on website", default=True,
        help_text="Untick to hide it without deleting it.",
    )
    order = models.PositiveIntegerField(
        default=0, help_text="Smaller numbers appear first. Items with the same number show newest first.",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order", "-created_at"]
        verbose_name = "portfolio item"
        verbose_name_plural = "portfolio"

    def __str__(self):
        return f"{self.title} ({self.get_category_display()})"

    def clean(self):
        if self.category == self.DESIGN and not self.image:
            raise ValidationError({"image": "Graphic design items need an image."})

    @property
    def initial(self):
        return (self.title[:1] or "?").upper()

    @property
    def stack_list(self):
        return [t.strip() for t in self.stack.split(",") if t.strip()]

    def save(self, *args, **kwargs):
        # A freshly uploaded file is not committed to storage yet.
        if self.image and not getattr(self.image, "_committed", True):
            self.image = optimise_image(self.image)
        super().save(*args, **kwargs)


@receiver(pre_save, sender=PortfolioItem)
def _remove_replaced_image(sender, instance, **kwargs):
    """When an image is swapped for another, delete the old file."""
    if not instance.pk:
        return
    try:
        old = sender.objects.get(pk=instance.pk).image
    except sender.DoesNotExist:
        return
    if old and old.name != instance.image.name:
        old.delete(save=False)


@receiver(post_delete, sender=PortfolioItem)
def _remove_deleted_image(sender, instance, **kwargs):
    if instance.image:
        instance.image.delete(save=False)
