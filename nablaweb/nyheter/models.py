from django.db import models
from django.contrib.auth.models import User

class News(models.Model):
    class Meta:
        verbose_name_plural = "news"
    
    user = models.ForeignKey(User)
    author_name = models.CharField(max_length=64, null=True, blank=True) # hvis annen forfatter enn brukeren som poster
    
    headline = models.CharField(max_length=64)
    lead_paragraph = models.TextField()
    main_text = models.TextField()
    pub_date = models.DateTimeField()
    
    def __unicode__(self):
        return self.headline
