#!/bin/bash

# Define the PostgreSQL user and database
POSTGRES_USER=sbyard
POSTGRES_DB=villager_server

# Define a list of fixtures
fixtures="users tokens players guest_players chess_clubs time_settings community_posts messages tournaments games"

# Use a for loop to iterate through the list
for fixture in $fixtures
do
    # Read the JSON content of the fixture file
    CONTENT=$(cat "/docker-entrypoint-initdb.d/fixtures/${fixture}.json")

    # Insert the JSON content into the corresponding table
    # Adjust the SQL command according to your actual table structure and data
    psql -U $POSTGRES_USER -d $POSTGRES_DB <<EOF
    INSERT INTO ${fixture} (data) VALUES ('${CONTENT}');
EOF
done