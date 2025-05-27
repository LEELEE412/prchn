from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
        ('accounts', '0006_usersubscription'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='subscirbed_saving_products',
            new_name='subscribed_saving_products',
        ),
    ]