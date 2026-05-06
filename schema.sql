-- Lazizjonning ikkinchi projecti: oddiy schema

-- Users jadvali
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
);

-- Orders jadvali
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id),
    product_name VARCHAR(100) NOT NULL,
    order_date TIMESTAMPTZ DEFAULT NOW()
