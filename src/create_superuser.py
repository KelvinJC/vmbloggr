from django.contrib.auth import get_user_model
UserModel = get_user_model()
if not UserModel.objects.filter(username='Admin').exists():
    user = UserModel.objects.create_user('Admin', password='Admin')
    user.is_superuser = True
    user.is_staff = True
    user.save()