import requests
import os
import pandas as pd
import json
import boto3
from source.cities import cities
from datetime import datetime
import pytz
import time
import logging
import awswrangler as wr

from dotenv import load_dotenv
load_dotenv()


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

bucket=os.getenv("S3_BUCKET")
region=os.getenv("AWS_DEFAULT_REGION")

today=datetime.utcnow()
def extract(API_KEY,cities=cities):
    logger.info("Starting extraction process")
    s3=boto3.client('s3',region_name=region)
    #bucket="weather-data-store"
    for city in cities:

            url = (
                f"https://api.openweathermap.org/data/2.5/weather"
                f"?q={city}"
                f"&appid={API_KEY}"
                f"&units=metric"
            )
            response = requests.get(url)
            data=response.json()
            if(data['cod']==200):
                logger.info(f"Extracting weather data for {city}")
                json_data=json.dumps(data)
                s3.put_object(Bucket=bucket,Key=f'weather/raw/{today.year}/{today.month:02d}/{today.day:02d}/{city}/data.json',Body=json_data)
                logger.info(
                    f"Successfully uploaded data for {city}"
                )

            elif(data['message'] == 'city not found'):
                logger.warning(
                    f"No valid data returned for {city}"
                )            
            else:
                logger.error(
                f"API key is Invalid"
                )
                return False
                
                            
 
    logger.info("Extraction process completed")
    return True
    
    
def transform(cities=cities):
    s3=boto3.client('s3',region_name=region)
    data={"id":[],"city":[],"cur_date":[], "weather":[], "temp":[], "feels_like":[], "temp_min":[], "temp_max":[], "wind_speed":[], "sunrise":[], "sunset":[]}
    for city in cities:
        prefix=f'weather/raw/{today.year}/{today.month:02d}/{today.day:02d}/{city}/data.json'
        response=s3.get_object(Bucket=bucket,Key=prefix)
        content=json.loads(response["Body"].read().decode("utf-8"))
        data["id"].append(content["id"])
        data["city"].append(city)
        data["cur_date"].append(datetime.fromtimestamp(content["dt"],pytz.timezone("Europe/Berlin")).date())
        data["weather"].append(content["weather"][0]["main"])
        data["temp"].append(content["main"]["temp"])    
        data["feels_like"].append(content["main"]["feels_like"])    
        data["temp_min"].append(content["main"]["temp_min"])
        data["temp_max"].append(content["main"]["temp_max"])    
        data["wind_speed"].append(content["wind"]["speed"])    
        data["sunrise"].append(str(datetime.fromtimestamp(content["sys"]["sunrise"],pytz.timezone("Europe/Berlin")).time()))    
        data["sunset"].append(str(datetime.fromtimestamp(content["sys"]["sunset"],pytz.timezone("Europe/Berlin")).time()))

    df= pd.DataFrame(data)
    df["year"] = str(today.year)
    df["month"] = f"{today.month:02d}"
    df["day"] = f"{today.day:02d}"
    return df
'''def load(df):
    validate(df)
    wr.s3.to_parquet(
        df=df,
        path=f"s3://{bucket}/weather/transformed/",
        dataset=True,
        mode="overwrite_partitions",
        partition_cols=["year", "month", "day"],
        database="weather",
        table="weather_details"
    )

    logger.info("Successfully loaded data into Athena")'''
def load(df):
    validate(df)

    path = f"s3://{bucket}/weather/transformed/"

    existing_df = wr.s3.read_parquet(
        path=path,
        dataset=True,
        partition_filter=lambda x:
            x["year"] == str(df["year"].iloc[0]) and
            x["month"] == str(df["month"].iloc[0]) and
            x["day"] == str(df["day"].iloc[0])
    )

    combined_df = pd.concat(
        [existing_df, df],
        ignore_index=True
    )

    combined_df = (
        combined_df
        .sort_values("cur_date")
        .drop_duplicates(subset=["id"], keep="last")
    )

    wr.s3.to_parquet(
        df=combined_df,
        path=path,
        dataset=True,
        mode="overwrite_partitions",
        partition_cols=["year", "month", "day"],
        database="weather",
        table="weather_details"
    )

    logger.info("Successfully loaded latest daily data")

def validate(df):
    assert df.cur_date.nunique()==1 and df.cur_date.iloc[0]==datetime.today().date(),"Date mismatch"
    assert df["city"].isna().all()==False, "City name error"
    
    
    
        
                 
