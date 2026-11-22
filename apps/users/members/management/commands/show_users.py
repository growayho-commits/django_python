from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Displays users first, then optionally allows Add, Edit, or Delete.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("\n=== USER LIST ==="))
        
        # முதலில் ரோல் வாரியாகவோ அல்லது அனைத்தையுமோ வடிகட்டி காட்ட
        role_filter = input("Enter role to filter (superuser, merchant, seller, executive, member) or press Enter for all: ").strip().lower()
        
        users = User.objects.all()
        if role_filter == 'superuser':
            users = users.filter(is_superuser=True)
        elif role_filter:
            users = users.filter(role=role_filter) if hasattr(User, 'role') else []

        count = users.count() if hasattr(users, 'count') else len(users)
        self.stdout.write(self.style.SUCCESS(f"\nTotal Users Found: {count}"))
        for u in users:
            role_val = getattr(u, 'role', 'Superuser' if u.is_superuser else 'User')
            self.stdout.write(f"ID: {u.id} | Username: {u.username} | Email: {getattr(u, 'email', 'N/A')} | Role: {role_val}")

        self.stdout.write("\n----------------------------------------")
        action = input("Do you want to [A]dd, [E]dit, [D]elete, or just press Enter to exit? ").strip().lower()

        if action == 'a':
            self.stdout.write("\n--- Add New User ---")
            username = input("Enter username: ").strip()
            email = input("Enter email: ").strip()
            password = input("Enter password: ").strip()
            role = input("Enter role (merchant, seller, executive, member, etc.): ").strip()
            try:
                user = User.objects.create_user(username=username, email=email, password=password)
                if hasattr(user, 'role') and role:
                    user.role = role
                    user.save()
                self.stdout.write(self.style.SUCCESS(f"User '{username}' added successfully!"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error: {e}"))

        elif action == 'e':
            self.stdout.write("\n--- Edit User ---")
            username = input("Enter username of the user to edit: ").strip()
            try:
                user = User.objects.get(username=username)
                new_email = input(f"Enter new email (current: {user.email}): ").strip()
                new_role = input(f"Enter new role (current: {getattr(user, 'role', 'N/A')}): ").strip()
                if new_email:
                    user.email = new_email
                if hasattr(user, 'role') and new_role:
                    user.role = new_role
                user.save()
                self.stdout.write(self.style.SUCCESS(f"User '{username}' updated successfully!"))
            except User.DoesNotExist:
                self.stdout.write(self.style.ERROR("User not found!"))

        elif action == 'd':
            self.stdout.write("\n--- Delete User ---")
            username = input("Enter username of the user to delete: ").strip()
            try:
                user = User.objects.get(username=username)
                confirm = input(f"Are you sure you want to delete '{username}'? (y/n): ").strip().lower()
                if confirm == 'y':
                    user.delete()
                    self.stdout.write(self.style.SUCCESS(f"User '{username}' deleted successfully!"))
                else:
                    self.stdout.write("Deletion cancelled.")
            except User.DoesNotExist:
                self.stdout.write(self.style.ERROR("User not found!"))
        else:
            self.stdout.write(self.style.SUCCESS("Exited. Thank you!"))