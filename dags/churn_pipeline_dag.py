"""DAG principal: pipeline ELT de churn Telecom X.

Flujo: extraccion desde API -> carga a Postgres (raw) -> dbt run -> dbt test.
"""
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

import sys
sys.path.append("/opt/airflow")
from ingestion.extract_api import run as run_ingestion  # noqa: E402

default_args = {
    "owner": "juan.yanaya",
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="telecom_churn_elt",
    description="Pipeline ELT de fuga de clientes (Telecom X)",
    default_args=default_args,
    start_date=datetime(2026, 1, 1),
    schedule="0 6 * * *",  # diario 06:00 UTC
    catchup=False,
    tags=["elt", "churn", "portfolio"],
) as dag:

    extract_and_load = PythonOperator(
        task_id="extract_and_load_raw",
        python_callable=run_ingestion,
    )

    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command="cd /opt/dbt && dbt run --profiles-dir .",
    )

    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command="cd /opt/dbt && dbt test --profiles-dir .",
    )

    extract_and_load >> dbt_run >> dbt_test
