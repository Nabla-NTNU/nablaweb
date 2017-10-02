from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    args = "<partial match of group name>"
    help = "Shows a list of members in the groups with matching name." + \
           "If no name is specified, show a list of groups"

    def handle(self, *args, **options):
        try:
            name = args[0]
            groups = Group.objects.filter(name__icontains=name)
            for g in groups:
                self.stdout.write("%s (%d)" % (g.name, g.user_set.count()))
                for u in g.user_set.all():
                    self.stdout.write("\t%s <%s> %s" % (u.get_full_name(), u.username, u.email))
                self.stdout.write("\n\n")
        except IndexError:
            self.stdout.write("Please specify group name")
            groups = Group.objects.all()
            for g in groups:
                self.stdout.write("%s (%d)" % (g.name, g.user_set.count()))
