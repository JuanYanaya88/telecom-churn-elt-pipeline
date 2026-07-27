-- Limpieza y tipado de los datos crudos de clientes
with source as (
    select * from {{ source('raw', 'customers') }}
)

select
    "customerID"                                  as customer_id,
    lower("Churn")                                as churn,
    "customer_gender"                             as gender,
    ("customer_SeniorCitizen")::int               as is_senior_citizen,
    "customer_tenure"::int                        as tenure_months,
    "phone_PhoneService"                          as phone_service,
    "internet_InternetService"                    as internet_service,
    "account_Contract"                            as contract_type,
    "account_PaymentMethod"                       as payment_method,
    nullif("account_Charges_Monthly"::text, '')::numeric as monthly_charges,
    nullif(trim("account_Charges_Total"::text), '')::numeric as total_charges
from source
where "customerID" is not null
