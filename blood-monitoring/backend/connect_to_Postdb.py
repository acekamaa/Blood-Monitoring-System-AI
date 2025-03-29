from sqlalchemy import create_engine
import pandas as pd

# PostgreSQL connection details
DB_USER = "postgres"
DB_PASSWORD = "123456789"
DB_HOST = "localhost"  
DB_PORT = "5432"
DB_NAME = "blood_monitoring"

# Create database connection
engine = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

# Load CSV and insert into PostgreSQL
df = pd.read_csv("C:/Users/kev/Desktop/Blood-Monitoring-System-AI/blood-monitoring/backend/dummydata/blood_type_dummy_data.csv")
columns = df.columns.tolist()
print("Columns in the CSV file:", columns)
df.to_sql("blood_data", engine, if_exists="replace", index=False)

print("Data successfully inserted into PostgreSQL.")
