# Movie Rental Data Warehouse Design

## Project Description

This project presents a Data Warehouse design for a movie rental business based on the Sakila OLTP database schema.

The OLTP system is used for daily operational activities such as managing customers, films, inventory, rentals, payments, staff, stores, and locations. However, an OLTP database is not optimized for analytical reporting and business decision-making.

For this reason, this project proposes a dimensional Data Warehouse model that helps managers analyze rental activity, revenue, film popularity, customer behavior, store performance, staff performance, return behavior, and time-based trends.

## Project Objective

The main objective of this project is to transform the OLTP movie rental schema into a Data Warehouse design using dimensional modeling principles.

The project focuses on:

- Identifying business questions that the Data Warehouse should answer.
- Designing suitable fact tables.
- Designing suitable dimension tables.
- Defining the grain of each fact table.
- Defining the main measures for each fact table.
- Creating a dimensional model diagram.
- Explaining the ETL process.
- Writing SQL scripts to create and load the Data Warehouse.
- Writing analytical SQL queries to answer business questions.
- Defining data quality rules.

## Data Warehouse Design Type

The proposed design uses a Star Schema with shared dimensions.

The main fact tables are:

- fact_rental
- fact_payment
- fact_return

The main dimension tables are:

- dim_date
- dim_customer
- dim_film
- dim_category
- dim_language
- dim_store
- dim_staff
- dim_location

## Fact Tables Description

### fact_rental

This fact table represents rental transactions.

It is used to analyze rental activity, film popularity, customer rental behavior, store rental performance, and staff rental activity.

Main measure:

- rental_count

### fact_payment

This fact table represents payment transactions.

It is used to analyze revenue by film, customer, store, staff member, location, and time.

Main measures:

- payment_amount
- payment_count

### fact_return

This fact table represents returned rental transactions.

It is used to analyze return behavior, rental duration, late returns, and films that are returned late most often.

Main measures:

- return_count
- rental_duration_days
- late_return_flag
- late_days

## Dimension Tables Description

### dim_date

Used to analyze rentals, payments, and returns by day, month, quarter, and year.

### dim_customer

Used to analyze customer behavior, customer activity, and customer revenue.

### dim_film

Used to analyze film popularity, film revenue, rental duration, rating, category, and language.

### dim_category

Used to analyze rental activity and revenue by film category.

### dim_language

Used to analyze films based on their language.

### dim_store

Used to compare store performance based on rentals and revenue.

### dim_staff

Used to analyze staff performance in rental and payment processing.

### dim_location

Used to support location-based analysis by city and country.

## Project Files

This repository includes the main files for the Movie Rental Data Warehouse project.

The report file contains the full project documentation, including the introduction, business questions, dimensional model design, dimensional model diagram, ETL design, data quality considerations, and conclusion.

The dimensional model diagram shows the proposed Star Schema and the relationships between the fact tables and dimension tables.

The SQL folder contains the scripts used to create the Data Warehouse tables, load data from the Sakila OLTP database, and run analytical queries.

The etl_pandas.py file contains the practical ETL implementation using Python and pandas. It reads data from the Sakila OLTP database, transforms the data, and loads it into the movie_rental_dw Data Warehouse.

The requirements.txt file lists the Python libraries needed to run the ETL script.



## SQL Files

The SQL folder includes the following files:

### create_tables.sql

This file creates the Data Warehouse database and tables.

It includes:

- Dimension tables
- Fact tables
- Primary keys
- Foreign keys


### analysis_queries.sql

This file contains analytical queries that answer business questions.

Examples of analysis include:

- Most rented films
- Films with the highest revenue
- Revenue by store
- Revenue by month
- Late returned films

## Report Sections

The report contains the following sections:

1. Introduction
2. Business Questions
3. Dimensional Model Design
4. Dimensional Model Diagram
5. ETL Design
6. Data Quality Considerations
7. Conclusion

## Sample Business Questions

The Data Warehouse can answer questions such as:

- Which films are rented most frequently?
- Which films generate the highest revenue?
- Which stores generate the highest revenue?
- How does revenue change by month, quarter, or year?
- Which films are returned late most often?
- What is the average rental duration for different films?
- Which customers rent the most films?
- Which staff members process the highest number of rentals or payments?

## Tools Used

- MySQL Server
- MySQL Workbench
- Sakila OLTP Database
- diagrams.net / draw.io
- Microsoft Word
- GitHub

## Expected Outcome

By using the proposed Data Warehouse, business managers can analyze operational movie rental data in a clear and useful way.

The Data Warehouse supports better reporting, better analysis, and better business decision-making by organizing the OLTP data into fact tables and dimension tables.

## Author

Prepared by: Aws Thafer 12220122

Course: Data Warehousing / Data Architecture