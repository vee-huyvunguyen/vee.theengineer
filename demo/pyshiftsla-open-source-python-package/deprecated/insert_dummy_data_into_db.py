from faker import Faker
from typing import List, Tuple
from datetime import datetime, timedelta, timezone
import random
import psycopg2
from os import getenv


def generate_dummy_data_daily(
    faker_instance: Faker,
    employees_emails: List[str],
    customers_emails: List[str],
    current_date: datetime,
    number_of_message_daily: int,
) -> List[dict]:
    """
    Generate dummy data for a single day.
    """
    datetime_message_sent_at = faker_instance.date_time_between_dates(
        datetime_start=current_date,
        datetime_end=current_date + timedelta(days=1),
    )
    message_sent_at = int(datetime_message_sent_at.timestamp())
    is_customer = random.choice([True, False])
    message_from = random.choice(customers_emails if is_customer else employees_emails)
    return [
        {
            "message_sent_at": message_sent_at,
            "is_customer": is_customer,
            "message_from": message_from,
            "session_order_in_date": random.randint(1, 20),
            "datetime": datetime_message_sent_at,
            "message": "Hello, Hi, How are you ?",
        }
        for _ in range(number_of_message_daily)
    ]


def generate_dummy_data(
    faker_instance: Faker,
    number_of_unique_employees_email: int,
    number_of_unique_customers_email: int,
    data_datetime_range: Tuple[datetime, datetime],
    number_of_message_daily: int,
) -> List[dict]:
    """
    Generate dummy customer service message data for a date range.
    """
    start_date, end_date = data_datetime_range
    employees_emails = [
        faker_instance.email() for _ in range(number_of_unique_employees_email)
    ]
    customers_emails = [
        faker_instance.email() for _ in range(number_of_unique_customers_email)
    ]

    # Generate a list of dates within the range
    date_range = [
        start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)
    ]

    # Use map to generate messages for each day
    daily_messages = map(
        lambda date: generate_dummy_data_daily(
            faker_instance,
            employees_emails,
            customers_emails,
            date,
            number_of_message_daily,
        ),
        date_range,
    )

    # Flatten the list of lists into a single list
    return [message for day_messages in daily_messages for message in day_messages]


def insert_data_into_postgres(data: List[dict], connection_params: dict):
    """
    Insert generated data into a PostgreSQL database.

    Args:
        data (List[dict]): List of messages to insert.
        connection_params (dict): Dictionary with PostgreSQL connection parameters.
    """
    connection = psycopg2.connect(**connection_params)
    cursor = connection.cursor()

    # Define the SQL insert query
    insert_query = """
        INSERT INTO customer_service.customer_service_messages (
            message_sent_at, is_customer, message_from, session_order_in_date, datetime, message
        ) VALUES (%s, %s, %s, %s, %s, %s);
    """

    # Prepare the data for insertion
    records = [
        (
            record["message_sent_at"],
            record["is_customer"],
            record["message_from"],
            record["session_order_in_date"],
            record["datetime"],
            record["message"],
        )
        for record in data
    ]
    print(f"Inserting {len(data)} customer support messages into the database")
    try:
        cursor.executemany(insert_query, records)
        connection.commit()
        print(f"Inserted {len(records)} records successfully.")
    except Exception as e:
        connection.rollback()
        print(f"Error inserting data: {e}")
    finally:
        cursor.close()
        connection.close()


# Example usage:
def main():
    faker = Faker()
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2023, 1, 7)

    # Generate dummy data
    dummy_data = generate_dummy_data(
        faker_instance=faker,
        number_of_unique_employees_email=5,
        number_of_unique_customers_email=50,
        data_datetime_range=(start_date, end_date),
        number_of_message_daily=5000,
    )

    # Insert dummy data into PostgreSQL
    db_params = {
        "host": "localhost",
        "dbname": getenv("POSTGRES_DB"),
        "user": getenv("POSTGRES_USER"),
        "password": getenv("POSTGRES_PASSWORD"),
        "port": getenv("POSTGRES_PORT"),
    }

    insert_data_into_postgres(dummy_data, db_params)

if __name__ == "__main__":
    main()