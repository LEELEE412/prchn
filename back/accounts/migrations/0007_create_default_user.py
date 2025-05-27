from django.db import migrations
from django.contrib.auth.hashers import make_password

def create_default_user(apps, schema_editor):
    User = apps.get_model('accounts', 'User')  # 또는 AUTH_USER_MODEL
    if not User.objects.filter(username='1234').exists():
        User.objects.create(
            username='1234',
            password=make_password('1234'),
            # 이메일 등 다른 필드가 필수라면 적절히 채워주세요
        )

class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_usersubscription'),
    ]

    operations = [
        migrations.RunPython(create_default_user),
    ]