from steps import insert_dummy_data_into_db
from dotenv import load_dotenv

load_dotenv("customer-service-dummy-db/.env")

if __name__ == "__main__":
    insert_dummy_data_into_db.execute()

