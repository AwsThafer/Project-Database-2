CREATE DATABASE IF NOT EXISTS movie_rental_dw;

USE movie_rental_dw;

CREATE TABLE IF NOT EXISTS dim_date (
    date_key INT PRIMARY KEY,
    full_date DATE,
    day_number INT,
    month_number INT,
    month_name VARCHAR(20),
    quarter_number INT,
    year_number INT,
    day_of_week VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS dim_customer (
    customer_key INT PRIMARY KEY,
    customer_id INT,
    customer_full_name VARCHAR(100),
    email VARCHAR(100),
    active_status VARCHAR(20),
    create_date DATE,
    city VARCHAR(100),
    country VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS dim_category (
    category_key INT PRIMARY KEY,
    category_id INT,
    category_name VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS dim_language (
    language_key INT PRIMARY KEY,
    language_id INT,
    language_name VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS dim_film (
    film_key INT PRIMARY KEY,
    film_id INT,
    title VARCHAR(255),
    release_year INT,
    rental_duration INT,
    rental_rate DECIMAL(10,2),
    length INT,
    replacement_cost DECIMAL(10,2),
    rating VARCHAR(20),
    category_key INT,
    language_key INT,
    FOREIGN KEY (category_key) REFERENCES dim_category(category_key),
    FOREIGN KEY (language_key) REFERENCES dim_language(language_key)
);

CREATE TABLE IF NOT EXISTS dim_store (
    store_key INT PRIMARY KEY,
    store_id INT,
    store_address VARCHAR(255),
    city VARCHAR(100),
    country VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS dim_staff (
    staff_key INT PRIMARY KEY,
    staff_id INT,
    staff_full_name VARCHAR(100),
    email VARCHAR(100),
    active_status VARCHAR(20),
    store_id INT
);

CREATE TABLE IF NOT EXISTS dim_location (
    location_key INT PRIMARY KEY,
    address VARCHAR(255),
    district VARCHAR(100),
    city VARCHAR(100),
    country VARCHAR(100),
    postal_code VARCHAR(20),
    phone VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS fact_rental (
    rental_fact_key INT PRIMARY KEY,
    date_key INT,
    customer_key INT,
    film_key INT,
    store_key INT,
    staff_key INT,
    location_key INT,
    rental_count INT,

    FOREIGN KEY (date_key) REFERENCES dim_date(date_key),
    FOREIGN KEY (customer_key) REFERENCES dim_customer(customer_key),
    FOREIGN KEY (film_key) REFERENCES dim_film(film_key),
    FOREIGN KEY (store_key) REFERENCES dim_store(store_key),
    FOREIGN KEY (staff_key) REFERENCES dim_staff(staff_key),
    FOREIGN KEY (location_key) REFERENCES dim_location(location_key)
);

CREATE TABLE IF NOT EXISTS fact_payment (
    payment_fact_key INT PRIMARY KEY,
    date_key INT,
    customer_key INT,
    film_key INT,
    store_key INT,
    staff_key INT,
    location_key INT,
    payment_amount DECIMAL(10,2),
    payment_count INT,

    FOREIGN KEY (date_key) REFERENCES dim_date(date_key),
    FOREIGN KEY (customer_key) REFERENCES dim_customer(customer_key),
    FOREIGN KEY (film_key) REFERENCES dim_film(film_key),
    FOREIGN KEY (store_key) REFERENCES dim_store(store_key),
    FOREIGN KEY (staff_key) REFERENCES dim_staff(staff_key),
    FOREIGN KEY (location_key) REFERENCES dim_location(location_key)
);

CREATE TABLE IF NOT EXISTS fact_return (
    return_fact_key INT PRIMARY KEY,
    date_key INT,
    customer_key INT,
    film_key INT,
    store_key INT,
    staff_key INT,
    location_key INT,
    return_count INT,
    rental_duration_days INT,
    late_return_flag INT,
    late_days INT,

    FOREIGN KEY (date_key) REFERENCES dim_date(date_key),
    FOREIGN KEY (customer_key) REFERENCES dim_customer(customer_key),
    FOREIGN KEY (film_key) REFERENCES dim_film(film_key),
    FOREIGN KEY (store_key) REFERENCES dim_store(store_key),
    FOREIGN KEY (staff_key) REFERENCES dim_staff(staff_key),
    FOREIGN KEY (location_key) REFERENCES dim_location(location_key)
);

SHOW TABLES;