CREATE SCHEMA customer_service;

CREATE TABLE customer_service.customer_service_messages (
    message_sent_at BIGINT NOT NULL,
    is_customer BOOLEAN NOT NULL,
    message_from VARCHAR(255) NOT NULL,
    session_order_in_date INT NOT NULL,
    datetime TIMESTAMP NOT NULL,
    message VARCHAR(255) NOT NULL
);