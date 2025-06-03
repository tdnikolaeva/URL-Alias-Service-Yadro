from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
import getpass

UserModel = get_user_model()


class Command(BaseCommand):
    help = 'Создает обычного пользователя с интерактивным вводом данных'

    def handle(self, *args, **options):
        self.stdout.write("Создание нового пользователя.")

        while True:
            username = input('Username: ').strip()
            if not username:
                self.stdout.write(self.style.ERROR('Username не может быть пустым. Попробуйте еще раз.'))
                continue
            if UserModel.objects.filter(username=username).exists():
                self.stdout.write(
                    self.style.ERROR(f"Пользователь с username '{username}' уже существует. Попробуйте другое имя."))
                continue
            break

        while True:
            password = getpass.getpass('Password: ')
            password2 = getpass.getpass('Password (повторите): ')
            if password != password2:
                self.stdout.write(self.style.ERROR("Пароли не совпадают. Попробуйте снова."))
                continue
            if not password:
                self.stdout.write(self.style.ERROR("Пароль не может быть пустым. Попробуйте снова."))
                continue
            try:
                validate_password(password)
            except ValidationError as e:
                self.stdout.write(self.style.ERROR(" ".join(e.messages)))
                continue
            break

        user = UserModel.objects.create_user(username=username, password=password)
        user.is_staff = False
        user.is_superuser = False
        user.save()

        self.stdout.write(self.style.SUCCESS(f"Пользователь '{username}' успешно создан."))
