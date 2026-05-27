import awswrangler as wr
from dotenv import load_dotenv
import os
load_dotenv()
region=os.getenv("AWS_DEFAULT_REGION")
ATHENA_BUCKET=os.getenv("S3_Athena_BUCKET")
def delete_old_glue_table():
    wr.catalog.delete_table_if_exists(
        database="weather",
        table="weather_details"
    )

    print("Old Glue table deleted")
    
def sample_query():
    df = wr.athena.read_sql_query(
        sql="SELECT * FROM weather.weather_details",
        database="weather",
        s3_output=f"s3://{ATHENA_BUCKET}/results/"
        )
    return df

print(sample_query())