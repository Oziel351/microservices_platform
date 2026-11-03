-- Create schemas for each service
CREATE SCHEMA IF NOT EXISTS product_schema;

-- Grant permissions to the app user
GRANT ALL PRIVILEGES ON SCHEMA product_schema TO admin;
