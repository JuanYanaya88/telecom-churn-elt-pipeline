-- Metricas de churn por tipo de contrato y servicio de internet
select
    contract_type,
    internet_service,
    count(*)                                          as total_customers,
    count(*) filter (where churn = 'yes')             as churned_customers,
    round(avg(monthly_charges), 2)                    as avg_monthly_charges,
    round(
        count(*) filter (where churn = 'yes')::numeric / count(*), 4
    )                                                 as churn_rate
from {{ ref('stg_customers') }}
where churn in ('yes', 'no')
group by 1, 2
