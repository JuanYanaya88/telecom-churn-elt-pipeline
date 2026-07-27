-- Dimension de clientes para consumo analitico
select
    customer_id,
    gender,
    is_senior_citizen,
    tenure_months,
    contract_type,
    payment_method,
    internet_service
from {{ ref('stg_customers') }}
