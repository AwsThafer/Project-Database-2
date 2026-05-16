USE movie_rental_dw;

-- 1. Most rented films
SELECT 
    f.title,
    SUM(fr.rental_count) AS total_rentals
FROM fact_rental fr
JOIN dim_film f ON fr.film_key = f.film_key
GROUP BY f.title
ORDER BY total_rentals DESC
LIMIT 10;

-- 2. Films with highest revenue
SELECT 
    f.title,
    SUM(fp.payment_amount) AS total_revenue
FROM fact_payment fp
JOIN dim_film f ON fp.film_key = f.film_key
GROUP BY f.title
ORDER BY total_revenue DESC
LIMIT 10;

-- 3. Revenue by store
SELECT 
    s.store_id,
    s.city,
    s.country,
    SUM(fp.payment_amount) AS total_revenue
FROM fact_payment fp
JOIN dim_store s ON fp.store_key = s.store_key
GROUP BY s.store_id, s.city, s.country
ORDER BY total_revenue DESC;

-- 4. Revenue by month
SELECT 
    d.year_number,
    d.month_number,
    d.month_name,
    SUM(fp.payment_amount) AS total_revenue
FROM fact_payment fp
JOIN dim_date d ON fp.date_key = d.date_key
GROUP BY d.year_number, d.month_number, d.month_name
ORDER BY d.year_number, d.month_number;

-- 5. Late returned films
SELECT 
    f.title,
    SUM(fr.late_return_flag) AS late_return_count,
    AVG(fr.rental_duration_days) AS average_rental_duration,
    SUM(fr.late_days) AS total_late_days
FROM fact_return fr
JOIN dim_film f ON fr.film_key = f.film_key
GROUP BY f.title
ORDER BY late_return_count DESC, total_late_days DESC
LIMIT 10;