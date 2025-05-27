from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('accounts', '0008_merge_20250527_1510'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usersubscription',
            name='product',
        ),
        migrations.AddField(
            model_name='usersubscription',
            name='content_type',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='usersubscription',
            name='object_id',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
    ]