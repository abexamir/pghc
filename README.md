# Health Check Service

This is a simple health check service written in Python that checks whether the current PostgreSQL instance is the master or not. It exposes an HTTP API endpoint at `/is_master` to indicate the status.

## Usage

### Running Locally
1. Ensure you have Python installed on your system.
2. Install the dependencies by running:
    ```
    pip install -r requirements.txt
    ```
3. Set the environment variables `POSTGRES_HOST`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, and `POSTGRES_DB` to connect to your PostgreSQL instance.
4. Run the health check service:
    ```
    python health_check.py
    ```

### Running with Docker
1. Build the Docker image by running:
    ```
    docker build -t health-check-service .
    ```
2. Run the Docker container, setting the required environment variables:
    ```
    docker run -d -p 8080:8080 --env POSTGRES_HOST=<YOUR_POSTGRES_HOST> --env POSTGRES_USER=<YOUR_POSTGRES_USER> --env POSTGRES_PASSWORD=<YOUR_POSTGRES_PASSWORD> --env POSTGRES_DB=<YOUR_POSTGRES_DB> health-check-service
    ```

## API Endpoint

### `/is_master`
- **Method**: GET
- **Description**: Checks if the current PostgreSQL node is the master.
- **Response**:
    - Status Code 200: If the node is the master.
    - Status Code 503: If the node is not the master.
    - Status Code 500: If an error occurs during the check.

## License

This project is licensed under the [MIT License](LICENSE).


