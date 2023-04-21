# Generated by Django 4.1.2 on 2023-04-19 14:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseModel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('last_updated_at', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Pharmacy',
            fields=[
                ('basemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='pharmacy.basemodel')),
                ('pharmacy_name', models.CharField(max_length=60)),
                ('pharmacy_profile_pic', models.ImageField(upload_to='pharmacy/profile/')),
                ('pharmacy_reg_no', models.CharField(max_length=20)),
                ('pharmacy_pincode', models.IntegerField()),
                ('pharmacy_city', models.CharField(max_length=60)),
                ('pharmacy_address', models.CharField(max_length=200)),
                ('pharmacy_description', models.TextField()),
                ('pharmacy_phone', models.CharField(max_length=60)),
                ('pharmacy_rating', models.FloatField(default=0)),
                ('is_verified', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='pharmacy_profile', to=settings.AUTH_USER_MODEL)),
            ],
            bases=('pharmacy.basemodel',),
        ),
        migrations.CreateModel(
            name='PharmaReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review', models.TextField()),
                ('user', models.CharField(max_length=60)),
                ('created_at', models.DateField(auto_now=True)),
                ('pharmacy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pharmacy_review', to='pharmacy.pharmacy')),
            ],
        ),
        migrations.CreateModel(
            name='PharmacyImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='pharmacy/images/')),
                ('pharmacy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pharmacy_images', to='pharmacy.pharmacy')),
            ],
        ),
    ]
