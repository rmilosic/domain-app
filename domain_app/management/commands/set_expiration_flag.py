from django.core.management.base import BaseCommand, CommandError
from domain_app.models import Domain, DomainFlag
from django.utils import timezone
from datetime import datetime, timedelta


class Command(BaseCommand):
    help = 'Sets domain flag to expired for all the domains with expiration date on the exact date'

    """    def add_arguments(self, parser):
        parser.add_argument('poll_ids', nargs='+', type=int)
    """
    def handle(self, *args, **options):
        # get all domain objects where expiration date is equal to today
           
        domains = Domain.objects.filter(
            exdate__gt=timezone.localdate() + timedelta(days=-1),
            exdate__lt=timezone.localdate() + timedelta(days=1)
            )
        
        for domain_item in domains:

            new_flag = DomainFlag(
                domain=domain_item, 
                flag='EXPIRED',
                valid_from=timezone.now()
                )
            new_flag.save()

        self.stdout.write(self.style.SUCCESS(f'Successfully changed flag to EXPIRED for {len(domains)} domains'))