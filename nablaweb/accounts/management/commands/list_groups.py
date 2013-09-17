from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import Group

class Command(BaseCommand):
    args = "<partial match of group name>"
    help = "Shows a list of groups with matching name"

    def handle(self, *args, **options):
        try:
            name = args[0]
            groups = Group.objects.filter(name__icontains=name)
        except IndexError:
            groups = Group.objects.all()
        for g in groups:
            self.stdout.write("%s (%d)" % (g.name, g.user_set.count()))
