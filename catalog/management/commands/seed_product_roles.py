from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from catalog.models import Product


class Command(BaseCommand):
    help = "Создаёт группу 'Модератор продуктов' с нужными правами"

    def handle(self, *args, **options):
        ct = ContentType.objects.get_for_model(Product)

        # Кастомное право (создаётся миграцией Meta.permissions)
        can_unpublish = Permission.objects.get(
            content_type=ct, codename="can_unpublish_product"
        )

        # Базовое модельное право удаления
        can_delete = Permission.objects.get(content_type=ct, codename="delete_product")

        group, _ = Group.objects.get_or_create(name="Модератор продуктов")
        group.permissions.set([can_unpublish, can_delete])
        group.save()

        self.stdout.write(
            self.style.SUCCESS(
                "Группа 'Модератор продуктов' настроена: права назначены."
            )
        )
