# Test Task 123123

This repository contains the Test Task for InlyIT, designed to demonstrate our development practices and deployment procedures.

Api spec in file openapi.json

!!! Replace values in .env file !!! 

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Dependencies

Dependencies are described in `requirements.txt`. Ensure you have them installed to run the project successfully.

### Installing

To install the dependencies from `requirements.txt`, run the following command:

```bash
pip install -r requirements.txt
```

Alternatively, you can build the Docker image which includes all necessary dependencies:

```bash
docker-compose build
```

### Executing program

To start the program, just run the bash script located at docker/app.sh:

```bash
bash docker/app.sh
```
Or, you can use docker-compose up to bring up a Docker container:

```bash
docker-compose up
```
