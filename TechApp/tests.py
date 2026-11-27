import io
import shutil
import tempfile

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from PIL import Image

from .models import PortfolioItem

TEMP_MEDIA = tempfile.mkdtemp()


def make_image(size=(2400, 1600), fmt="PNG"):
    buf = io.BytesIO()
    Image.new("RGB", size, (46, 91, 77)).save(buf, format=fmt)
    return SimpleUploadedFile(f"shot.{fmt.lower()}", buf.getvalue(), content_type=f"image/{fmt.lower()}")


@override_settings(MEDIA_ROOT=TEMP_MEDIA)
class PortfolioTests(TestCase):
    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(TEMP_MEDIA, ignore_errors=True)
        super().tearDownClass()

    def test_pages_load(self):
        for name in ("index", "about", "service", "portfolio", "contact"):
            self.assertEqual(self.client.get(reverse(name)).status_code, 200, name)

    def test_upload_is_resized_and_converted(self):
        item = PortfolioItem.objects.create(
            title="Shop", category=PortfolioItem.WEB, summary="x", image=make_image())
        self.assertTrue(item.image.name.endswith(".webp"))
        with Image.open(item.image.path) as im:
            self.assertLessEqual(max(im.size), 1600)

    def test_only_published_items_are_listed(self):
        PortfolioItem.objects.create(title="Visible one", category=PortfolioItem.WEB, summary="a")
        PortfolioItem.objects.create(title="Hidden one", category=PortfolioItem.WEB, summary="b", is_published=False)
        html = self.client.get(reverse("portfolio")).content.decode()
        self.assertIn("Visible one", html)
        self.assertNotIn("Hidden one", html)

    def test_design_requires_image(self):
        from django.core.exceptions import ValidationError
        item = PortfolioItem(title="Logo", category=PortfolioItem.DESIGN, summary="brief")
        with self.assertRaises(ValidationError):
            item.full_clean()

    def test_stack_list(self):
        item = PortfolioItem(title="x", summary="y", stack="Django,  Bootstrap , ,PWA")
        self.assertEqual(item.stack_list, ["Django", "Bootstrap", "PWA"])

    def test_replaced_image_is_removed(self):
        item = PortfolioItem.objects.create(title="A", category=PortfolioItem.WEB, summary="x", image=make_image())
        old = item.image.path
        item.image = make_image((800, 600))
        item.save()
        import os
        self.assertFalse(os.path.exists(old))
