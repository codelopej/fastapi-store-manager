# FastAPI Store Manager

[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![REST API](https://img.shields.io/badge/REST%20API-005571?style=for-the-badge&logo=swagger&logoColor=white)](https://swagger.io/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![SQLModel](https://img.shields.io/badge/SQLModel-1F425F?style=for-the-badge&logo=sqlalchemy&logoColor=white)](https://sqlmodel.tiangolo.com/)

FastAPI Store Manager is a powerful and scalable API for managing a product store. Built with FastAPI and SQLModel, this API allows you to efficiently handle products, categories. Whether you are building a small shop or a large-scale marketplace, FastAPI Store Manager provides the robust foundation you need.

## Features

- **Product Management**: Add, update, delete, and retrieve product details.
- **Category Management**: Organize products into categories for better navigation.
- **Database Integration**: Utilize SQLModel for seamless database operations.
- **Extensible**: Easily extend and customize the API to fit your specific needs.

## Getting Started

To get started with FastAPI Store Manager, follow these steps:

1. install the required dependencies:

```bash
pip install -r requirements.txt
```

2. Create a `.env` file in the root directory and add the following environment variables:
For example:
ENV="environment_here_(development, production, ...)"
DATABASE_URL="your_database_url_here"
DATABASE_SHOULD_SEEDED="should_be_true_or_false_here"
DATABASE_SHOULD_MIGRATED="should_be_true_or_false_here"

3. Run the following command to create the database tables:

```bash
python -m app.database.migrations.update
```

4. Run the project with the following command:

```bash
fastapi run app/main.py --reload
```

## Contributions

Contributions are welcome! Feel free to open issues and submit pull requests to help improve this project.
