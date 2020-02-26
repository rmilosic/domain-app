from datetime import datetime, timedelta
from io import StringIO

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Domain, DomainFlag
from django.core.management import call_command

def create_new_domain(fqdn, erdate=None, exdate=None):
    """
    Create a new domain with fqdn, created date is now() with timezone
    """
    return Domain.objects.create(fqdn=fqdn, erdate=erdate, exdate=exdate)


def create_domain_flag(domain, flag, valid_from=timezone.now(), valid_to=None):
    """
    Create a new domain flag with args `domain` (domain instance), `flag` (choice) and
    default `valid_from` is timezone.now()
    """
    return DomainFlag.objects.create(domain=domain, valid_from=valid_from, valid_to=valid_to)



class DomainIndexTests(TestCase):
    def test_no_domains(self):
        """
        If no domains exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No active domains")

    def test_new_domain(self):
        """
        If new domain is added with no additional arguments, it should appear
        """
        create_new_domain(fqdn="testdomain.cz")
        response = self.client.get(reverse('index'))
        self.assertQuerysetEqual(
            response.context['domains'], ['<Domain: testdomain.cz>']
        )

    def test_expired_domain(self):
        """
        If domain is added with an expired date of today, it should not be seen
        """
        create_new_domain(fqdn="testdomain.cz", exdate=timezone.localdate())
        response = self.client.get(reverse('index'))
        self.assertQuerysetEqual(
            response.context['domains'], []
        )

    def test_erased_domain(self):
        """
        If domain is added with an erased datetime of now, it should not be seen
        """
        create_new_domain(fqdn="testdomain.cz", erdate=timezone.now())
        response = self.client.get(reverse('index'))
        self.assertQuerysetEqual(
            response.context['domains'], []
        )


class DomainDetailTests(TestCase):
    def test_no_flags(self):
        """
        If a domain is created without any flags, no active flags should appear
        """
        new_domain = create_new_domain(fqdn="testdomain.cz")
        # create_domain_flag(domain=new_domain, flag="EXPIRED")
        response = self.client.get(reverse('detail', args=[new_domain.id]))
        self.assertQuerysetEqual(
            response.context['flags'], []
        )
    
    def test_with_future_flag(self):
        """
        If a domain_flag is created with `valid_from` in the future, the flag should not be seen
        """
        new_domain = create_new_domain(fqdn="testdomain.cz")
        create_domain_flag(domain=new_domain, flag="EXPIRED", valid_from=timezone.now()+timedelta(days=+1))
        response = self.client.get(reverse('detail', args=[new_domain.id]))
        self.assertQuerysetEqual(
            response.context['flags'], []
        )

    def test_with_now_valid_flag(self):
        """
        If a domain_flag is created with `valid_from` in the past, the flag should be seen
        """
        new_domain = create_new_domain(fqdn="testdomain.cz")
        create_domain_flag(domain=new_domain, flag="EXPIRED", valid_from=timezone.now()+timedelta(days=-1))
        response = self.client.get(reverse('detail', args=[new_domain.id]))
        self.assertQuerysetEqual(
            response.context['flags'], ['<DomainFlag: id: testdomain.cz flag:EXPIRED valid from:2020-02-23 valid to: None>']
        )

    def test_with_past_valid_flag(self):
        """
        If a domain_flag is created with `valid_from` and `valid_to` in the past, the flag should not be seen
        """
        new_domain = create_new_domain(fqdn="testdomain.cz")
        create_domain_flag(
            domain=new_domain, 
            flag="EXPIRED", 
            valid_from=timezone.now()+timedelta(days=-5),
            valid_to=timezone.now()+timedelta(days=-1)
            )
        response = self.client.get(reverse('detail', args=[new_domain.id]))
        self.assertQuerysetEqual(
            response.context['flags'], []
        )


class SetExpirationFlagTests(TestCase):
    def test_set_expiration_flag(self):
        """
        Create a domain with expiration date as of today, then run the `set_expiration_flag.py` 
        management command. Assert if a correct `domain_flag` was created
        """
        new_domain = create_new_domain(fqdn="testdomain.cz", exdate=timezone.localdate())

        out = StringIO()
        call_command('set_expiration_flag', stdout=out)

        domain_flags = DomainFlag.objects.filter(domain=new_domain)

        self.assertQuerysetEqual(
            domain_flags, ['<DomainFlag: id: testdomain.cz flag:EXPIRED valid from:2020-02-24 valid to: None>']
        )


        