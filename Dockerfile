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
ENTRYPOINT [ "./entrypoint.sh" ]

# Expose port
EXPOSE 8000

#CHECK