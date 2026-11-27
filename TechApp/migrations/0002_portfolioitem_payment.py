import TechApp.models
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TechApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(max_length=255)),
                ('payer_id', models.CharField(max_length=255)),
                ('status', models.CharField(max_length=50)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payer_name', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='PortfolioItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120)),
                ('category', models.CharField(choices=[('web', 'Website or system'), ('design', 'Graphic design')], default='web', max_length=10)),
                ('tag', models.CharField(blank=True, help_text='Websites: the industry, e.g. Education. Designs: the kind of piece, e.g. Logo or Flyer.', max_length=60, verbose_name='Industry or type')),
                ('summary', models.TextField(help_text='Websites: a short summary of what it does. Designs: the client brief.', max_length=600, verbose_name='Description')),
                ('notes', models.TextField(blank=True, help_text='Designs only. Shown beside the large preview.', max_length=600, verbose_name='Colour and branding notes')),
                ('stack', models.CharField(blank=True, help_text='Websites only. Separate with commas, e.g. Django, Bootstrap, M-Pesa.', max_length=200, verbose_name='Built with')),
                ('url', models.URLField(blank=True, help_text='Websites only. Leave empty if it is not live yet.', verbose_name='Live site address')),
                ('image', models.ImageField(blank=True, help_text='Screenshot (websites) or the finished design. JPG, PNG or WebP, up to 8 MB. It is resized and compressed automatically.', upload_to='portfolio/%Y/%m/', validators=[django.core.validators.FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp', 'gif']), TechApp.models.validate_image_size])),
                ('is_published', models.BooleanField(default=True, help_text='Untick to hide it without deleting it.', verbose_name='Show on website')),
                ('order', models.PositiveIntegerField(default=0, help_text='Smaller numbers appear first. Items with the same number show newest first.')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'portfolio item',
                'verbose_name_plural': 'portfolio',
                'ordering': ['order', '-created_at'],
            },
        ),
    ]
