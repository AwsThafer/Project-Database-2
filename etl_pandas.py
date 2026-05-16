import pandas as pd
from urllib.parse import quote_plus
from sqlalchemy import create_engine, text
# Database connection settings
USER = "root"
PASSWORD = "Root@12345"
HOST = "127.0.0.1"
PORT = "3306"

OLTP_DB = "sakila"
DW_DB = "movie_rental_dw"

# Encode password because it contains special characters like @
ENCODED_PASSWORD = quote_plus(PASSWORD)

# Create database engines
oltp_engine = create_engine(
    f"mysql+pymysql://{USER}:{ENCODED_PASSWORD}@{HOST}:{PORT}/{OLTP_DB}"
)

dw_engine = create_engine(
    f"mysql+pymysql://{USER}:{ENCODED_PASSWORD}@{HOST}:{PORT}/{DW_DB}"
)
def load_table(table_name):
    """Read a full table from the Sakila OLTP database."""
    return pd.read_sql(f"SELECT * FROM {table_name}", oltp_engine)


def clear_dw_tables():
    """Clear Data Warehouse tables before loading new data."""
    tables = [
        "fact_return",
        "fact_payment",
        "fact_rental",
        "dim_film",
        "dim_location",
        "dim_staff",
        "dim_store",
        "dim_language",
        "dim_category",
        "dim_customer",
        "dim_date",
    ]

    with dw_engine.begin() as conn:
        conn.execute(text("SET FOREIGN_KEY_CHECKS = 0;"))
        for table in tables:
            conn.execute(text(f"TRUNCATE TABLE {table};"))
        conn.execute(text("SET FOREIGN_KEY_CHECKS = 1;"))


def create_date_dimension(rental, payment):
    """Create dim_date from rental_date, return_date, and payment_date."""

    rental_dates = rental[["rental_date"]].rename(columns={"rental_date": "full_date"})
    return_dates = rental[["return_date"]].rename(columns={"return_date": "full_date"})
    payment_dates = payment[["payment_date"]].rename(columns={"payment_date": "full_date"})

    dim_date = pd.concat([rental_dates, return_dates, payment_dates], ignore_index=True)
    dim_date = dim_date.dropna()
    dim_date["full_date"] = pd.to_datetime(dim_date["full_date"]).dt.date
    dim_date = dim_date.drop_duplicates()

    dim_date["full_date_dt"] = pd.to_datetime(dim_date["full_date"])
    dim_date["date_key"] = dim_date["full_date_dt"].dt.strftime("%Y%m%d").astype(int)
    dim_date["day_number"] = dim_date["full_date_dt"].dt.day
    dim_date["month_number"] = dim_date["full_date_dt"].dt.month
    dim_date["month_name"] = dim_date["full_date_dt"].dt.month_name()
    dim_date["quarter_number"] = dim_date["full_date_dt"].dt.quarter
    dim_date["year_number"] = dim_date["full_date_dt"].dt.year
    dim_date["day_of_week"] = dim_date["full_date_dt"].dt.day_name()

    dim_date = dim_date[
        [
            "date_key",
            "full_date",
            "day_number",
            "month_number",
            "month_name",
            "quarter_number",
            "year_number",
            "day_of_week",
        ]
    ]

    return dim_date.sort_values("date_key")

def create_dim_customer(customer, address, city, country):
    customer = customer[[
        "customer_id", "first_name", "last_name", "email",
        "active", "create_date", "address_id"
    ]]

    address = address[["address_id", "city_id"]]
    city = city[["city_id", "city", "country_id"]]
    country = country[["country_id", "country"]]

    df = customer.merge(address, on="address_id", how="left")
    df = df.merge(city, on="city_id", how="left")
    df = df.merge(country, on="country_id", how="left")

    dim_customer = pd.DataFrame()
    dim_customer["customer_key"] = df["customer_id"]
    dim_customer["customer_id"] = df["customer_id"]
    dim_customer["customer_full_name"] = df["first_name"] + " " + df["last_name"]
    dim_customer["email"] = df["email"]
    dim_customer["active_status"] = df["active"].apply(
        lambda x: "Active" if x == 1 else "Inactive"
    )
    dim_customer["create_date"] = pd.to_datetime(df["create_date"]).dt.date
    dim_customer["city"] = df["city"]
    dim_customer["country"] = df["country"]

    return dim_customer

def create_dim_category(category):
    dim_category = pd.DataFrame()
    dim_category["category_key"] = category["category_id"]
    dim_category["category_id"] = category["category_id"]
    dim_category["category_name"] = category["name"]
    return dim_category


def create_dim_language(language):
    dim_language = pd.DataFrame()
    dim_language["language_key"] = language["language_id"]
    dim_language["language_id"] = language["language_id"]
    dim_language["language_name"] = language["name"]
    return dim_language


def create_dim_film(film, film_category):
    df = film.merge(film_category, on="film_id", how="left")

    dim_film = pd.DataFrame()
    dim_film["film_key"] = df["film_id"]
    dim_film["film_id"] = df["film_id"]
    dim_film["title"] = df["title"]
    dim_film["release_year"] = df["release_year"]
    dim_film["rental_duration"] = df["rental_duration"]
    dim_film["rental_rate"] = df["rental_rate"]
    dim_film["length"] = df["length"]
    dim_film["replacement_cost"] = df["replacement_cost"]
    dim_film["rating"] = df["rating"]
    dim_film["category_key"] = df["category_id"]
    dim_film["language_key"] = df["language_id"]

    return dim_film.drop_duplicates(subset=["film_key"])

def create_dim_store(store, address, city, country):
    store = store[["store_id", "address_id"]]
    address = address[["address_id", "address", "city_id"]]
    city = city[["city_id", "city", "country_id"]]
    country = country[["country_id", "country"]]

    df = store.merge(address, on="address_id", how="left")
    df = df.merge(city, on="city_id", how="left")
    df = df.merge(country, on="country_id", how="left")

    dim_store = pd.DataFrame()
    dim_store["store_key"] = df["store_id"]
    dim_store["store_id"] = df["store_id"]
    dim_store["store_address"] = df["address"]
    dim_store["city"] = df["city"]
    dim_store["country"] = df["country"]

    return dim_store
def create_dim_staff(staff):
    dim_staff = pd.DataFrame()
    dim_staff["staff_key"] = staff["staff_id"]
    dim_staff["staff_id"] = staff["staff_id"]
    dim_staff["staff_full_name"] = staff["first_name"] + " " + staff["last_name"]
    dim_staff["email"] = staff["email"]
    dim_staff["active_status"] = staff["active"].apply(
        lambda x: "Active" if x == 1 else "Inactive"
    )
    dim_staff["store_id"] = staff["store_id"]

    return dim_staff

def create_dim_location(address, city, country):
    address = address[[
        "address_id", "address", "district",
        "city_id", "postal_code", "phone"
    ]]
    city = city[["city_id", "city", "country_id"]]
    country = country[["country_id", "country"]]

    df = address.merge(city, on="city_id", how="left")
    df = df.merge(country, on="country_id", how="left")

    dim_location = pd.DataFrame()
    dim_location["location_key"] = df["address_id"]
    dim_location["address"] = df["address"]
    dim_location["district"] = df["district"]
    dim_location["city"] = df["city"]
    dim_location["country"] = df["country"]
    dim_location["postal_code"] = df["postal_code"]
    dim_location["phone"] = df["phone"]

    return dim_location

def create_fact_rental(rental, inventory, customer):
    df = rental.merge(inventory, on="inventory_id", how="left")
    df = df.merge(customer[["customer_id", "address_id"]], on="customer_id", how="left")

    fact_rental = pd.DataFrame()
    fact_rental["rental_fact_key"] = df["rental_id"]
    fact_rental["date_key"] = pd.to_datetime(df["rental_date"]).dt.strftime("%Y%m%d").astype(int)
    fact_rental["customer_key"] = df["customer_id"]
    fact_rental["film_key"] = df["film_id"]
    fact_rental["store_key"] = df["store_id"]
    fact_rental["staff_key"] = df["staff_id"]
    fact_rental["location_key"] = df["address_id"]
    fact_rental["rental_count"] = 1

    return fact_rental


def create_fact_payment(payment, rental, inventory, customer):
    df = payment.merge(rental[["rental_id", "inventory_id"]], on="rental_id", how="left")
    df = df.merge(inventory, on="inventory_id", how="left")
    df = df.merge(customer[["customer_id", "address_id"]], on="customer_id", how="left")

    fact_payment = pd.DataFrame()
    fact_payment["payment_fact_key"] = df["payment_id"]
    fact_payment["date_key"] = pd.to_datetime(df["payment_date"]).dt.strftime("%Y%m%d").astype(int)
    fact_payment["customer_key"] = df["customer_id"]
    fact_payment["film_key"] = df["film_id"]
    fact_payment["store_key"] = df["store_id"]
    fact_payment["staff_key"] = df["staff_id"]
    fact_payment["location_key"] = df["address_id"]
    fact_payment["payment_amount"] = df["amount"]
    fact_payment["payment_count"] = 1

    return fact_payment


def create_fact_return(rental, inventory, film, customer):
    df = rental.dropna(subset=["return_date"]).copy()
    df = df.merge(inventory, on="inventory_id", how="left")
    df = df.merge(film[["film_id", "rental_duration"]], on="film_id", how="left")
    df = df.merge(customer[["customer_id", "address_id"]], on="customer_id", how="left")

    df["rental_date"] = pd.to_datetime(df["rental_date"])
    df["return_date"] = pd.to_datetime(df["return_date"])
    df["rental_duration_days"] = (df["return_date"] - df["rental_date"]).dt.days
    df["late_return_flag"] = (df["rental_duration_days"] > df["rental_duration"]).astype(int)
    df["late_days"] = df["rental_duration_days"] - df["rental_duration"]
    df["late_days"] = df["late_days"].apply(lambda x: x if x > 0 else 0)

    fact_return = pd.DataFrame()
    fact_return["return_fact_key"] = df["rental_id"]
    fact_return["date_key"] = df["return_date"].dt.strftime("%Y%m%d").astype(int)
    fact_return["customer_key"] = df["customer_id"]
    fact_return["film_key"] = df["film_id"]
    fact_return["store_key"] = df["store_id"]
    fact_return["staff_key"] = df["staff_id"]
    fact_return["location_key"] = df["address_id"]
    fact_return["return_count"] = 1
    fact_return["rental_duration_days"] = df["rental_duration_days"]
    fact_return["late_return_flag"] = df["late_return_flag"]
    fact_return["late_days"] = df["late_days"]

    return fact_return


def load_to_dw(df, table_name):
    df.to_sql(
        table_name,
        dw_engine,
        if_exists="append",
        index=False,
        chunksize=1000,
    )
    print(f"Loaded {len(df)} rows into {table_name}")


def main():
    print("Reading OLTP tables from Sakila database...")

    rental = load_table("rental")
    payment = load_table("payment")
    customer = load_table("customer")
    film = load_table("film")
    inventory = load_table("inventory")
    store = load_table("store")
    staff = load_table("staff")
    address = load_table("address")
    city = load_table("city")
    country = load_table("country")
    category = load_table("category")
    film_category = load_table("film_category")
    language = load_table("language")

    print("Creating Data Warehouse tables using pandas transformations...")

    dim_date = create_date_dimension(rental, payment)
    dim_customer = create_dim_customer(customer, address, city, country)
    dim_category = create_dim_category(category)
    dim_language = create_dim_language(language)
    dim_film = create_dim_film(film, film_category)
    dim_store = create_dim_store(store, address, city, country)
    dim_staff = create_dim_staff(staff)
    dim_location = create_dim_location(address, city, country)

    fact_rental = create_fact_rental(rental, inventory, customer)
    fact_payment = create_fact_payment(payment, rental, inventory, customer)
    fact_return = create_fact_return(rental, inventory, film, customer)

    print("Clearing old Data Warehouse data...")
    clear_dw_tables()

    print("Loading dimensions...")
    load_to_dw(dim_date, "dim_date")
    load_to_dw(dim_customer, "dim_customer")
    load_to_dw(dim_category, "dim_category")
    load_to_dw(dim_language, "dim_language")
    load_to_dw(dim_film, "dim_film")
    load_to_dw(dim_store, "dim_store")
    load_to_dw(dim_staff, "dim_staff")
    load_to_dw(dim_location, "dim_location")

    print("Loading fact tables...")
    load_to_dw(fact_rental, "fact_rental")
    load_to_dw(fact_payment, "fact_payment")
    load_to_dw(fact_return, "fact_return")

    print("ETL completed successfully using Python and pandas.")


if __name__ == "__main__":
    main()