from django.db import models

# Create your models here.


class QrEvent(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    

    def get_name(self):
        return self.name


class QrTicket(models.Model):
    event = models.ForeignKey(QrEvent, on_delete=models.CASCADE)
    email = models.EmailField(blank=False)
    
    def get_email(self):
        return self.email

    def __str__(self):
        return self.email
