from models import load, transform, extract
import awswrangler as wr
import os
from dotenv import load_dotenv
load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")

def run_pipeline(API_KEY=API_KEY):
    ex=extract(API_KEY)
    if(ex):
        df=transform()
        print(df)
        load(df)
    
if __name__=="__main__":
    run_pipeline()
