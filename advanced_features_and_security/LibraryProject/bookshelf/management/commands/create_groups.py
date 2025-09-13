from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from bookshelf.models import Book

class Command(BaseCommand):
    help = "Create groups and assign permissions"

    def handle(self, *args, **kwargs):
        # Define groups
        groups_permissions = {
            "Admins": ["can_view", "can_create", "can_edit", "can_delete"],
            "Editors": ["can_view", "can_create", "can_edit"],
            "Viewers": ["can_view"],
        }

        book_content_type = ContentType.objects.get_for_model(Book)

        for group_name, perms in groups_permissions.items():
            group, created = Group.objects.get_or_create(name=group_name)
            for perm_code in perms:
                try:
                    perm = Permission.objects.get(codename=perm_code, content_type=book_content_type)
                    group.permissions.add(perm)
                except Permission.DoesNotExist:
                    self.stdout.write(self.style.ERROR(f"Permission {perm_code} not found"))
            group.save()
            self.stdout.write(self.style.SUCCESS(f"Group {group_name} created/updated"))
