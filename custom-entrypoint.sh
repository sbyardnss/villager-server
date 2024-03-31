#!/bin/bash

# Check if PG_INIT is set and remove the PG_INIT file if it exists
if [ "$PG_INIT" = "1" ]; then
    rm -f /var/lib/postgresql/data/PG_INIT
fi

# Execute the original entrypoint script
exec /usr/local/bin/docker-entrypoint.sh postgres