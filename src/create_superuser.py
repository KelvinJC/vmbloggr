from django.contrib.auth import get_user_model
UserModel = get_user_model()
user = UserModel.objects.create_user('Admin', password='Admin')
user.is_superuser = True
user.is_staff = True
user.save()