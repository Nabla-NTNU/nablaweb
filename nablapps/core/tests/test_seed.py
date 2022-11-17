from django.test import TestCase

from nablapps.core.management.commands.seed import (
    ALL_SEEDERS,
    NabladSeeder,
    perform_seed,
)


def preserve(seeders=ALL_SEEDERS):
    perform_seed(seeders, delete=False, create=True)


def delete(seeders=ALL_SEEDERS):
    perform_seed(seeders, delete=True, create=False)


def seed(seeders=ALL_SEEDERS):
    perform_seed(seeders, delete=True, create=True)


def assert_exists(exists: bool, /, seeders=ALL_SEEDERS) -> None:
    for seeder in seeders:
        # Allow failing to create Nablad because of the ImageMagick dependency
        if exists and seeder is NabladSeeder:
            continue
        assert seeder.exists() == exists, seeder.short_description


class TestSeed(TestCase):
    def test_seed_from_empty(self):
        assert_exists(False)

        seed()

        assert_exists(True)

    def test_preserve_from_empty(self):
        assert_exists(False)

        preserve()

        assert_exists(True)

    def test_delete_from_empty(self):
        assert_exists(False)

        delete()

        assert_exists(False)

    def test_complex(self):
        assert_exists(False)

        preserve()
        assert_exists(True)

        seed()
        assert_exists(True)

        delete()
        assert_exists(False)
