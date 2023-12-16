# Docker Django Socialmedia App API

This is a sample Django project configured to run within a Docker container. It includes all necessory config files to facilitate easy deployment and development.

## Getting Started

These instructions will help you run the project locally on your machine.

### Prerequisites

Make sure you have the following installed on your machine:

- Docker
- Docker Compose

### Running the Project

1. Clone the repository to your local machine:

   ```bash
   git clone <repository-url>
   cd <repository-directory>

2. Build and run the Docker container:

    ```bash
    docker-compose up --build

This command will build the Docker image, create a container, and start the Django development server.

3. Access the application in your browser:

    Open your browser and navigate to http://localhost:8023.

    You should see your Django application up and running.



## Getting Started
To access the Django admin panel, you can go to http://localhost:8023/admin. The default credentials are:

Username: root
Password: Admin@123