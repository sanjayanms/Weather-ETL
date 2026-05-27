import os
import sys
from datetime import datetime
from dotenv import load_dotenv
from airflow.operators.python import PythonOperator

sys.path.append('/opt/airflow/weather_analysis')

from source.models import extract, transform, load
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta


# Add project path inside container
load_dotenv("/opt/airflow/weather_analysis/.env")



# Default DAG arguments
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

# Main pipeline function
def run_weather_pipeline():
    """
    Executes the complete ETL pipeline:
    Extract -> Transform -> Load
    """
    API_KEY = os.getenv("OPENWEATHER_API_KEY")

    ex=extract(API_KEY)
    if(ex):
        df=transform()
        load(df)

# Define DAG
with DAG(
    dag_id="weather_etl_pipeline",
    default_args=default_args,
    description="Weather ETL Pipeline using Airflow",
    start_date=datetime(2026, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=["etl", "weather", "aws"],
) as dag:

    run_pipeline_task = PythonOperator(
        task_id="run_weather_pipeline",
        python_callable=run_weather_pipeline,
    )

    run_pipeline_task