from django.core.management.base import BaseCommand, CommandError
from gallery.models import Album

class Command(BaseCommand):
    args = '<album_id album_id ...>'
    help = 'Delete the album and all its pictures.'

    def handle(self, *args, **options):
        for album_id in args:
            try:
                album = Album.objects.get(pk=int(album_id))
            except Poll.DoesNotExist:
                raise CommandError('Album "%s" does not exist' % album_id)

            album.delete()

            self.stdout.write('Successfully deleted Album "%s"\n' % album_id)

