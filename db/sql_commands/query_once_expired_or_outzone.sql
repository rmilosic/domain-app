SELECT domain.*
FROM 
public.domain_flag as domain_flag
LEFT JOIN public.domain as domain ON 
domain_flag.domain_id = domain.id
WHERE 
    domain_flag.flag IN ('EXPIRED', 'OUTZONE')