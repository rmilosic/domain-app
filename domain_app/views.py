from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.db.models import Q
from django.utils import timezone
from django.db.models import Prefetch

from .models import Domain, DomainFlag


def index(request):
    """list of distinct existing domains and their active flags """

    domains = Domain.objects.distinct().filter(exdate__isnull=True, erdate__isnull=True).prefetch_related(Prefetch('domainflag', queryset=DomainFlag.objects.filter(
        Q(valid_to__gt=timezone.now()) | Q(valid_to__isnull=True),
        valid_from__lte=timezone.now()))).order_by('crdate')
    return render(request, 'domain_app/index.html', {'domains': domains})


def detail(request, id):
    domain = get_object_or_404(Domain, pk=id)
    active_domain_flags = DomainFlag.objects.filter(
        Q(valid_to__gt=timezone.now()) | Q(valid_to__isnull=True),
        domain=domain.id, 
        valid_from__lte=timezone.now()
    )
    return render(request, 'domain_app/detail.html', {'domain': domain, 'flags': active_domain_flags})