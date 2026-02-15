from drf_spectacular.utils import extend_schema, OpenApiExample
from rest_framework import status
from rest_framework.authtoken.serializers import AuthTokenSerializer

register_schema = extend_schema(
    tags=['Auth'],
    auth=[],
    summary="Register a new user",
    description="Creates a new account. Returns the created user data",
    responses={
        201: "User created successfully",
        400: "Validation error",
    },
    examples=[
        OpenApiExample(
            'Registration Request',
            description='Data sent by the user',
            value={
                'username': 'Marchello',
                'email': 'marchello@example.com',
                'password': 'strong_password_123'
            },
            request_only=True,
        ),
        OpenApiExample(
            'Success Response',
            description='Data returned by the server',
            value={
                'id': 15,
                'username': 'Marchello',
                'email': 'marchello@example.com',
                'storage_limit': 104857600,
                'used_storage': 0
            },
            response_only=True,
            status_codes=['201']
        ),
        OpenApiExample(
            'Validation Error',
            description='Example of validation failure',
            value={
                'username': ['A user with that username already exists'],
                'password': ['This password is too short']
            },
            response_only=True,
            status_codes=['400']
        )
    ]
)

login_schema = extend_schema(
    tags=['Auth'],
    auth=[],
    summary="Login / Obtain Token",
    description="Returns an API Token",
    request={'application/json': AuthTokenSerializer},
    responses={
        200: "Token generated",
        400: "Error",
    },
    examples=[
        OpenApiExample(
            'Login Request',
            value={
                'username': 'Marchello',
                'password': 'strong_password_123'
            },
            request_only=True,
        ),
        OpenApiExample(
            'Token Response',
            description='The API Token you need to use in headers',
            value={
                'token': '9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b'
            },
            response_only=True,
            status_codes=['200']
        ),
        OpenApiExample(
            'Login Error',
            value={
                'non_field_errors': ['Unable to log in with provided credentials']
            },
            response_only=True,
            status_codes=['400']
        )
    ]
)