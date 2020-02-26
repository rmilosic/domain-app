SELECT DISTINCT ON (domain.id) domain.id,
domain.fqdn, domain.crdate, domain.erdate
FROM
public.domain as domain
FULL OUTER JOIN public.domain_flag as domain_flag ON
domain.id = domain_flag.domain_id
WHERE 
    domain.erdate IS NULL AND
    (domain_flag.flag != 'EXPIRED' OR
    domain_flag.flag IS NULL OR
    (domain_flag.valid_to < now() OR domain_flag.valid_from > now()
    ));
