<img width="2524" height="1434" alt="Group 10" src="https://github.com/user-attachments/assets/aa226528-58d8-4147-a42d-ad768db6d9f4" />

ByteDrive is a high-performance Media Archive API designed for secure cloud storage

> [!CAUTION]
> Running this project via Docker on Windows may lead to high RAM consumption by the VmmemWSL process. It is recommended to limit WSL 2 memory usage in your .wslconfig file to prevent the Docker Engine from consuming all available system resources

## Technology Stack:

* Django & Django REST Framework - main framework for building the API
* Docker - platform for containerizing the application
* PostgreSQL - relational database for storing users, pets, and their actions
* Django ORM - built-in ORM for working with the database
* rest_framework.authtoken - authentication and endpoint protection

## Key Features:

* **User registration and authentication** using TokenAuthentication
* **CRUD operations for file management**: upload, retrieve, update, and delete files
* **Metadata tracking**: Automatically store and manage file properties and timestamps
* **Endpoint protection**: Strict access control where users manage only their own data
* **API documentation**: Integrated Swagger UI via drf-spectacular.
* **Cascade deletion**: Automated cleanup of all user-related files and data upon account deletion

## Getting Started:

### 1. Clone the repository

```bash
git clone https://github.com/Marchello-Projects/ByteDrive
```

### 2. Set up environment variables

Create a `.env` file in the root directory with the following content:

```env
# Django Settings
SECRET_KEY=your_generated_secret_key

# Database Settings
DB_NAME=bytedrive
DB_USER=postgres
DB_PASSWORD=your_secure_password
DB_HOST=db

# Superuser Initial Data
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@example.com
DJANGO_SUPERUSER_PASSWORD=admin_password

# Python Settings
PYTHONDONTWRITEBYTECODE=1
PYTHONUNBUFFERED=1
```

> [!NOTE]
> **Generate a Secret Key**:
> Run the following command in your terminal to generate a new secure key:
> ```bash
> python3 -c 'import secrets; print(secrets.token_urlsafe(50))'
> # On Windows: python -c "import secrets; print(secrets.token_urlsafe(50))"
> ```

### 3. Prepare Entrypoint

> [!WARNING]
> If you are on Windows, ensure the entrypoint.sh file uses LF (Linux) line endings instead of CRLF. In VS Code, you can change this in the bottom right corner of the editor

### 4. Build and Run with Docker

Execute the following command to build the images and start the containers in detached mode:

```bash
docker-compose up -d --build
```

The system will automatically:

1. Start the PostgreSQL database
2. Wait for the database to be ready
3. Apply all database migrations
4. Automatically create a superuser using credentials from your `.env` file
5. Start the Django development server at `http://localhost:8000`

### 5. API Documentation

Once the containers are running, you can access the interactive API documentation at:

* **Swagger UI**: [http://localhost:8000/api/docs/]()
