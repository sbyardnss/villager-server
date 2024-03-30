# FROM python:3.9-slim

# RUN pip install --upgrade pip

# COPY ./requirements.txt .
# RUN pip install -r requirements.txt

# COPY . /villager_chess_api
# WORKDIR /villager_chess_api

# COPY ./entrypoint.sh .
# ENTRYPOINT [ "sh", "./entrypoint.sh" ]
FROM python:3.9-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# Copy project
COPY . /villager_chess_api
WORKDIR /villager_chess_api

# Copy entrypoint script
COPY ./entrypoint.sh .
RUN chmod +x ./entrypoint.sh

# Copy load_fixtures.sh script and make it executable
COPY ./villager_chess_api/fixtures/load_fixtures.sh /docker-entrypoint-initdb.d/
RUN chmod +x /docker-entrypoint-initdb.d/load_fixtures.sh

ENTRYPOINT [ "./entrypoint.sh" ]

# Expose port
EXPOSE 8000

#CHECK