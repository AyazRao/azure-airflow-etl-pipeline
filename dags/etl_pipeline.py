from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
}

with DAG(
    dag_id='azure_etl_pipeline',
    default_args=default_args,
    schedule_interval=None,  # Change to '0 12 * * *' for daily schedule
    catchup=False,
    tags=['azure', 'etl'],
) as dag:

    extract = BashOperator(
        task_id='extract_data',
        bash_command='python ~/airflow/scripts/extract_data.py',
    )

    transform = BashOperator(
        task_id='transform_data',
        bash_command='python ~/airflow/scripts/transform_data.py',
    )

    load = BashOperator(
        task_id='load_data',
        bash_command='python ~/airflow/scripts/load_to_sql.py',
    )

    # Set task order: extract → transform → load
    extract >> transform >> load
