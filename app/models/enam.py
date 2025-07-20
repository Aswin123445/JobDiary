from enum import Enum


class AuthProvider(str, Enum):
    email = "email"
    google = "google"
    github = "github"