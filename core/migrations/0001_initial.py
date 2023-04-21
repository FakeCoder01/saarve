# Generated by Django 4.1.2 on 2023-04-19 14:41

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('doctor', '0001_initial'),
        ('app', '0001_initial'),
        ('pharmacy', '0001_initial'),
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
            name='Payment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('last_updated_at', models.DateField(auto_now=True)),
                ('amount', models.FloatField()),
                ('method', models.CharField(default='online', max_length=8)),
                ('status', models.CharField(default='Initiated', max_length=10)),
                ('is_verified', models.BooleanField(default=False)),
                ('payment_id', models.CharField(default='3caX3xsM3N', max_length=10, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('last_updated_at', models.DateField(auto_now=True)),
                ('appointment_date_time', models.DateTimeField()),
                ('no_in_queuee', models.PositiveIntegerField(default=1)),
                ('patient_name', models.CharField(blank=True, max_length=60, null=True)),
                ('patient_age', models.PositiveIntegerField(blank=True, null=True)),
                ('patient_gender', models.CharField(default='Male', max_length=8)),
                ('note', models.TextField(blank=True, null=True)),
                ('schedule', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='schedule_appointment_details', to='doctor.doctorschedule')),
            ],
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('basemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.basemodel')),
                ('appointment', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='appointment_booking_detials', to='core.payment')),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='doctor_booking_profile', to='doctor.doctor')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='patient_booking_profile', to='app.userprofile')),
                ('payment', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='payment_booking_details', to='core.payment')),
                ('pharmacy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pharmacy_booking_profile', to='pharmacy.pharmacy')),
            ],
            bases=('core.basemodel',),
        ),
    ]
