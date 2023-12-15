## How to setup

### For instructions on how to install Poetry, visit [Poetry Installation Guide](https://python-poetry.org/docs/#installation).

To set up the project, follow these steps:
1. Clone the repository from GitHub.
2. Install the required dependencies using 
    ```bash 
    poetry install
    ```
3. Add autohooks to the project by running
    ```bash
    poetry run autohooks activate --mode poetry
    ```
4. Enable the autohook plugin for the project.

## How to start server

To start the server, run the following command:
```bash
python -m src.main
```

## How to run using Docker

To run the project using Docker, follow these steps:
1. Build the Docker image using `docker build -t myproject .`.
2. Run the Docker container using `docker run -p 9025:9025 myproject`.



## How to access Swagger to call API

To access Swagger and call the API, open a web browser and go to `http://localhost:8000/docs/`.
