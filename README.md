# Weather ETL Pipeline on AWS

# 🌦️ Weather ETL Pipeline using AWS, Airflow & Athena

A cloud-native ETL pipeline that extracts real-time weather data of major German cities from the OpenWeather API, transforms the raw JSON data into analytics-ready datasets, and stores the transformed output as Parquet files in Amazon S3 for querying through AWS Athena.

This project demonstrates practical Data Engineering concepts including:

* API data ingestion
* Cloud storage using AWS S3
* Data transformation with Pandas
* Parquet optimization for analytics
* Workflow orchestration using Apache Airflow
* Docker-based deployment
* Serverless querying with AWS Athena
* AWS Glue Catalog integration

---

# 📌 Project Architecture

```text
                +-------------------+
                | OpenWeather API   |
                +-------------------+
                          |
                          v
                +-------------------+
                | Extract Layer     |
                | Python + Requests |
                +-------------------+
                          |
                          v
                +-------------------+
                | Amazon S3         |
                | Raw JSON Storage  |
                +-------------------+
                          |
                          v
                +-------------------+
                | Transform Layer   |
                | Pandas            |
                +-------------------+
                          |
                          v
                +-------------------+
                | Amazon S3         |
                | Parquet Dataset   |
                +-------------------+
                          |
                          v
                +-------------------+
                | AWS Glue Catalog  |
                +-------------------+
                          |
                          v
                +-------------------+
                | AWS Athena        |
                | SQL Query Engine  |
                +-------------------+
                          |
                          v
                +-------------------+
                | Apache Airflow    |
                | DAG Scheduling    |
                +-------------------+
```

---

# 🚀 Features

✅ Extracts weather data from the OpenWeather API
✅ Stores raw API responses as JSON in Amazon S3
✅ Transforms weather data into structured tabular format
✅ Converts transformed data into optimized Parquet files
✅ Partitioned dataset structure for efficient querying
✅ Queries data using AWS Athena
✅ Automated orchestration using Apache Airflow
✅ Dockerized setup for reproducibility
✅ Logging and error handling included

---

# 🛠️ Tech Stack

| Category               | Technologies           |
| ---------------------- | ---------------------- |
| Cloud Platform         | AWS                    |
| Storage                | Amazon S3              |
| Query Engine           | AWS Athena             |
| Metadata Catalog       | AWS Glue               |
| Workflow Orchestration | Apache Airflow         |
| Programming Language   | Python                 |
| Containerization       | Docker, Docker Compose |
| Data Processing        | Pandas                 |
| AWS SDK                | Boto3, AWS Wrangler    |
| File Format            | JSON, Parquet          |

---

# 📂 Project Structure

```text
Weather-ETL/
│
├── airflow/
│   └── dags/
│       └── etl_dag.py
│
├── source/
│   ├── main.py
│   ├── models.py
│   ├── cities.py
│   └── misc.py
│
├── Installation/
│   ├── AWS_policy_example.json
│   └── Readme.txt
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── run.sh
└── .env
```

---

# ⚙️ ETL Pipeline Workflow

## 1. Extract

* Fetches weather data for multiple cities using the OpenWeather API.
* Uses Python `requests` library.
* Stores raw responses as JSON files in Amazon S3.

### Raw S3 Path

```text
s3://<bucket-name>/weather/raw/YYYY/MM/DD/<city>/data.json
```

---

## 2. Transform

The transformation layer:

* Reads raw JSON files from S3
* Extracts useful weather attributes
* Converts timestamps to readable date/time
* Structures data into Pandas DataFrames
* Adds partition columns (`year`, `month`, `day`)

### Extracted Fields

* City
* Weather condition
* Temperature
* Feels like temperature
* Min/Max temperature
* Wind speed
* Sunrise/Sunset time
* Current date

---

## 3. Load

The transformed data is:

* Converted into Parquet format
* Stored in Amazon S3
* Registered in AWS Glue Catalog
* Queried through AWS Athena

### Transformed S3 Path

```text
s3://<bucket-name>/weather/transformed/
```

### Athena Table

```sql
SELECT *
FROM weather.weather_details
LIMIT 10;
```

---

# 🔄 Airflow Orchestration

Apache Airflow orchestrates the entire ETL workflow.

### DAG Details

| Property    | Value                  |
| ----------- | ---------------------- |
| DAG ID      | `weather_etl_pipeline` |
| Schedule    | Daily                  |
| Retry Logic | Enabled                |
| Executor    | LocalExecutor          |

The DAG performs:

```text
Extract → Transform → Load
```

---

# 🐳 Dockerized Deployment

The project uses Docker Compose to deploy:

* Apache Airflow Webserver
* Airflow Scheduler
* PostgreSQL Metadata Database

### Start the Pipeline

```bash
docker compose up -d
```

### Access Airflow UI

```text
http://localhost:8080
```

Default credentials:

```text
Username: admin
Password: admin
```

---

# ☁️ AWS Services Used

| AWS Service    | Purpose                          |
| -------------- | -------------------------------- |
| Amazon S3      | Raw and transformed data storage |
| AWS Athena     | Serverless SQL querying          |
| AWS Glue       | Metadata catalog management      |
| IAM            | Secure AWS access permissions    |
| EC2 (Optional) | Deployment environment           |

---

# 🔐 IAM Permissions

The project includes an example IAM policy:

```text
Installation/AWS_policy_example.json
```

Permissions required:

* S3 Read/Write access
* Athena query execution
* Glue catalog access

---

# 🧪 Sample Athena Query

```sql
SELECT city,
       weather,
       temp,
       wind_speed
FROM weather.weather_details
WHERE year='2026'
LIMIT 20;
```

---

# 📦 Installation Guide

## 1. Clone Repository

```bash
git clone <your-repository-url>
cd Weather-ETL
```

---

## 2. Create AWS Resources

Create:

* S3 bucket for weather data
* S3 bucket for Athena query results

---

## 3. Configure Environment Variables

Create a `.env` file:

```env
OPENWEATHER_API_KEY=your_api_key
AWS_DEFAULT_REGION=your_region
S3_BUCKET=your_weather_bucket
S3_ATHENA_BUCKET=your_athena_bucket
AIRFLOW_SECRET_KEY=your_secret_key
```

---

## 4. Start Containers

```bash
docker compose up --build
```

---

## 5. Trigger DAG

* Open Airflow UI
* Enable `weather_etl_pipeline`
* Trigger DAG manually or wait for scheduled execution

---

# 📈 Data Engineering Concepts Demonstrated

This project showcases:

* End-to-end ETL pipeline design
* Data lake architecture concepts
* Cloud-native data engineering
* Batch processing workflows
* Workflow orchestration
* Data partitioning strategy
* Columnar storage optimization using Parquet
* Serverless analytics with Athena
* Infrastructure containerization

---

# 🔮 Future Improvements

Potential enhancements:

* CI/CD pipeline using GitHub Actions
* Terraform infrastructure provisioning
* Real-time streaming with Kafka/Kinesis
* Data quality checks with Great Expectations
* Monitoring & alerting with CloudWatch
* Incremental loading strategy
* Unit and integration testing
* Dashboard visualization using Power BI or Tableau

---

# 👨‍💻 Author

Built as a hands-on Data Engineering & Cloud project to demonstrate practical ETL pipeline development using AWS services.

---

# ⭐ If You Like This Project

Feel free to:

* Star the repository
* Fork the project
* Share feedback
* Connect on LinkedIn
