# Laburapy

Laburapy is a Python-based project designed for handling job applications. It combines modern web technologies for the front-end with a robust back-end task management system using Celery.

## Table of Contents

- [Project Overview](#project-overview)
- [Repository Structure](#repository-structure)
- [Setup and Installation](#setup-and-installation)
- [Dependencies](#dependencies)
- [Usage](#usage)
- [Module Documentation](#module-documentation)
  - [applications/](#applications)
  - [blog/](#blog)
  - [celeryworker/](#celeryworker)
  - [static/](#static)
  - [templates/](#templates)
  - [docker-compose.yml](#docker-composeyml)
  - [Dockerfile](#dockerfile)
  - [manage.py](#managepy)
  - [requirements.txt](#requirementstxt)
  - [secret.json](#secretjson)
- [Interrelations](#interrelations)
- [Contributing](#contributing)
- [License](#license)

## Project Overview

Laburapy is intended to streamline the job application process. It features a web interface for users to interact with and a back-end that handles various tasks such as email notifications and data processing using Celery.

## Repository Structure

- `applications/`: Main application logic.
- `blog/`: Blog-related functionalities.
- `celeryworker/`: Celery configurations and tasks.
- `static/`: Static files (CSS, JS, images).
- `templates/`: HTML templates for the web interface.
- `docker-compose.yml`: Docker Compose configuration.
- `Dockerfile`: Docker configuration for containerizing the application.
- `manage.py`: Django's command-line utility for administrative tasks.
- `requirements.txt`: Project dependencies.
- `secret.json`: Sensitive configuration details (keep secure).

## Setup and Installation

To set up and run Laburapy, follow these steps:

1. Clone the repository:
    ```sh
    git clone https://github.com/yamil95/laburapy.git
    cd laburapy
    ```

2. Build the Docker containers:
    ```sh
    docker-compose up --build
    ```

3. Access the application via the specified localhost port.

## Dependencies

Install project dependencies using:
```sh
pip install -r requirements.txt
