from django.db import models
from django.contrib import admin


class Domain(models.Model):
    fqdn = models.CharField(max_length=255, null=False)
    crdate = models.DateTimeField(auto_now=True)
    erdate = models.DateTimeField(null=True, blank=True)
    exdate = models.DateField(null=True, blank=True)
    class Meta:
        db_table = 'domain'
    
    def __str__(self):
        return f"{self.fqdn}"

class FlagType(models.TextChoices):
    EXPIRED = 'EXPIRED'
    OUTZONE = 'OUTZONE'
    DELETE_CANDIDATE  = 'DELETE_CANDIDATE'

class DomainFlag(models.Model):
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE, related_name='domainflag')
    flag = models.CharField(max_length=16, choices=FlagType.choices, default='EXPIRED')
    valid_from = models.DateTimeField(null=False)
    valid_to = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = 'domain_flag'

    def __str__(self):
        return f"id: {self.domain} flag:{self.flag} valid from:{self.valid_from.strftime('%Y-%m-%d')} valid to: {self.valid_to}"


admin.site.register(Domain)
admin.site.register(DomainFlag)