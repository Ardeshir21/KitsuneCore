# Dockerfile.dev

# Use a specific Python version
FROM postgres:17-bookworm

# Copy the SQL script to create a user and assign privileges
COPY ./docker/database/init.sql /docker-entrypoint-initdb.d/

# This will automatically run the SQL scripts during container initialization
# and will create the user with full privileges.

# By default, this image runs PostgreSQL as the user "postgres"
