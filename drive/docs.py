from drf_spectacular.utils import OpenApiExample, extend_schema
from rest_framework.authtoken.serializers import AuthTokenSerializer

from .serializers import (MediaFileSerializer, MediaFileUpdateSerializer,
                          RegisterSerializer)

not_found_example = OpenApiExample(
    "Not Found",
    value={"detail": "Not found."},
    response_only=True,
    status_codes=["404"],
)

bad_request_example = OpenApiExample(
    "Bad Request - Validation Error",
    value={
        "detail": "Validation error",
        "username": ["A user with that username already exists."],
        "email": ["Enter a valid email address."],
        "password": [
            "This password is too short. It must contain at least 8 characters."
        ],
    },
    response_only=True,
    status_codes=["400"],
)

bad_request_file_example = OpenApiExample(
    "Bad Request - File Upload Error",
    value={
        "detail": "Validation error",
        "file": ["No file was submitted."],
        "title": ["This field is required."],
    },
    response_only=True,
    status_codes=["400"],
)

register_schema = extend_schema(
    tags=["Auth"],
    auth=[],
    summary="Register a new user",
    description="Creates a new account. Returns the created user data",
    responses={
        201: RegisterSerializer,
        400: "Validation error",
    },
    examples=[
        OpenApiExample(
            "Registration Request",
            value={
                "username": "Marchello",
                "email": "marchello@example.com",
                "password": "strong_password_123",
            },
            request_only=True,
        ),
        OpenApiExample(
            "Success Response",
            value={
                "id": 15,
                "username": "Marchello",
                "email": "marchello@example.com",
                "storage_limit": 104857600,
                "used_storage": 0,
                "is_staff": False,
            },
            response_only=True,
            status_codes=["201"],
        ),
        bad_request_example,
    ],
)

login_schema = extend_schema(
    tags=["Auth"],
    auth=[],
    summary="Login / Obtain Token",
    description="Returns an API Token",
    request={"application/json": AuthTokenSerializer},
    responses={
        200: {"token": "string"},
        400: "Validation error / Invalid credentials",
    },
    examples=[
        OpenApiExample(
            "Token Response",
            value={"token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"},
            response_only=True,
            status_codes=["200"],
        ),
        OpenApiExample(
            "Invalid credentials",
            value={"detail": "Unable to log in with provided credentials."},
            response_only=True,
            status_codes=["400"],
        ),
    ],
)

profile_schema = extend_schema(
    tags=["Auth"],
    summary="Get User Profile",
    description="Returns details about the currently logged-in user.",
    responses={200: RegisterSerializer},
    examples=[
        OpenApiExample(
            "User Profile",
            value={
                "id": 15,
                "username": "Marchello",
                "email": "marchello@example.com",
                "storage_limit": 104857600,
                "used_storage": 2048576,
                "is_staff": False,
            },
            response_only=True,
            status_codes=["200"],
        )
    ],
)

file_list_schema = extend_schema(
    tags=["Files"],
    summary="List files",
    description="Get a list of all your uploaded files.",
    responses={200: MediaFileSerializer(many=True)},
)

file_create_schema = extend_schema(
    tags=["Files"],
    summary="Upload file",
    description="Upload a new file to your storage.",
    request={
        "multipart/form-data": {
            "type": "object",
            "properties": {
                "file": {"type": "string", "format": "binary"},
                "title": {"type": "string"},
                "description": {"type": "string"},
                "is_public": {"type": "boolean"},
            },
            "required": ["file", "title"],
        }
    },
    responses={201: MediaFileSerializer, 400: "Validation Error"},
    examples=[bad_request_file_example],
)

admin_all_files_schema = extend_schema(
    tags=["Admin"],
    summary="List ALL files (Admin only)",
    description="Shows all files from all users. Requires admin staff permissions.",
    responses={
        200: MediaFileSerializer(many=True),
        401: "Authentication credentials were not provided.",
        403: "You do not have permission to perform this action.",
    },
    examples=[
        OpenApiExample(
            "Forbidden",
            value={"detail": "You do not have permission to perform this action."},
            response_only=True,
            status_codes=["403"],
        ),
        OpenApiExample(
            "Unauthorized",
            value={"detail": "Authentication credentials were not provided."},
            response_only=True,
            status_codes=["401"],
        ),
    ],
)

file_update_schema = extend_schema(
    tags=["Files"],
    summary="Update File Info",
    description="Update title, description or visibility.",
    request=MediaFileUpdateSerializer,
    responses={
        200: MediaFileSerializer,
        400: "Validation error",
        404: "File not found",
    },
    examples=[
        OpenApiExample(
            "Success Update",
            value={
                "id": 15,
                "owner": "Marchello",
                "file": "http://127.0.0.1:8000/media/uploads/2026/02/16/my_photo.jpg",
                "title": "New Title",
                "description": "Updated description",
                "size": 2048576,
                "created_at": "2026-02-16T15:53:23.629909Z",
                "is_public": False,
            },
            response_only=True,
            status_codes=["200"],
        ),
        bad_request_example,
        not_found_example,
    ],
)

file_delete_schema = extend_schema(
    tags=["Files"],
    summary="Delete File",
    description="Delete the file permanently to free up space.",
    responses={204: None, 404: "File not found"},
    examples=[not_found_example],
)
