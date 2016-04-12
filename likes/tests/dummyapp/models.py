from django.db import models


class DummyModel(models.Model):
    def __str__(self):
        return str(self.id)
