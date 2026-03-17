# Generated manually for OTP, item details, multiple images

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jewels', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='otp',
            field=models.CharField(blank=True, max_length=6, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='otp_created_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='item',
            name='description',
            field=models.TextField(blank=True, help_text='Additional details about the item', null=True),
        ),
        migrations.AddField(
            model_name='item',
            name='video_url',
            field=models.URLField(blank=True, help_text='Optional video URL (YouTube, etc.)', null=True),
        ),
        migrations.CreateModel(
            name='ItemImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='items/extras/')),
                ('order', models.PositiveIntegerField(default=0)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='extra_images', to='jewels.item')),
            ],
            options={
                'ordering': ['order'],
            },
        ),
    ]
