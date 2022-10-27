from django.test import TestCase

from nablapps.core.management.commands.seed import ALL_SEEDERS, perform_seed


def seed(seeders=ALL_SEEDERS):
    perform_seed(seeders, delete=False, recreate=False)


def delete(seeders=ALL_SEEDERS):
    perform_seed(seeders, delete=True, recreate=False)


def recreate(seeders=ALL_SEEDERS):
    perform_seed(seeders, delete=False, recreate=True)


def assert_exists(exists: bool, /, seeders=ALL_SEEDERS) -> None:
    for seeder in seeders:
        assert seeder.exists() == exists, seeder.short_description


class TestSeed(TestCase):
    def test_seed_from_empty(self):
        assert_exists(False)

        seed()

        assert_exists(True)

    def test_delete_from_empty(self):
        assert_exists(False)

        delete()

        assert_exists(False)

    def test_recreate_from_empty(self):
        assert_exists(False)

        recreate()

        assert_exists(True)

    def test_complex(self):
        assert_exists(False)

        seed()
        assert_exists(True)

        recreate()
        assert_exists(True)

        delete()
        assert_exists(False)
