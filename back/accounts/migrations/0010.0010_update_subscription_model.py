from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_update_user_subscription_model'),
    ]

    operations = [
        migrations.RunSQL('DELETE FROM accounts_usersubscription;'),
    ]