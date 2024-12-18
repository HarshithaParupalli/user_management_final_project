import uuid
import pytest
from pydantic import ValidationError
from datetime import datetime
from app.schemas.user_schemas import UserBase, UserCreate, UserUpdate, UserResponse, UserListResponse, LoginRequest, UserProfileUpdate

# Fixtures for common test data
@pytest.fixture
def user_base_data():
    return {
        "nickname": "alex_smith_456",
        "email": "alex.smith@example.com",
        "first_name": "Alex",
        "last_name": "Smith",
        "role": "AUTHENTICATED",
        "bio": "I am a web developer with over 7 years of experience.",
        "profile_picture_url": "https://example.com/profile_pictures/alex_smith.jpg",
        "linkedin_profile_url": "https://linkedin.com/in/alexsmith",
        "github_profile_url": "https://github.com/alexsmith"
    }

@pytest.fixture
def user_create_data(user_base_data):
    return {**user_base_data, "password": "SecurePassword789!"}

@pytest.fixture
def user_update_data():
    return {
        "email": "alex.smith.new@example.com",
        "nickname": "a_smith",
        "first_name": "Alex",
        "last_name": "Smith",
        "bio": "I specialize in full-stack development with React and Django.",
        "profile_picture_url": "https://example.com/profile_pictures/alex_smith_updated.jpg"
    }

@pytest.fixture
def user_response_data(user_base_data):
    return {
        "id": uuid.uuid4(),
        "nickname": user_base_data["nickname"],
        "first_name": user_base_data["first_name"],
        "last_name": user_base_data["last_name"],
        "role": user_base_data["role"],
        "email": user_base_data["email"],
        "links": []
    }

@pytest.fixture
def login_request_data():
    return {"email": "alex_smith_456@emai.com", "password": "SecurePassword789!"}

# Tests for UserBase
def test_user_base_valid(user_base_data):
    user = UserBase(**user_base_data)
    assert user.nickname == user_base_data["nickname"]
    assert user.email == user_base_data["email"]

# Tests for UserCreate
def test_user_create_valid(user_create_data):
    user = UserCreate(**user_create_data)
    assert user.nickname == user_create_data["nickname"]
    assert user.password == user_create_data["password"]

def test_user_create_invalid_email(user_create_data):
    user_create_data["email"] = "invalid-email"
    with pytest.raises(ValidationError):
        UserCreate(**user_create_data)

# Tests for UserUpdate
def test_user_update_valid(user_update_data):
    user_update = UserUpdate(**user_update_data)
    assert user_update.email == user_update_data["email"]
    assert user_update.first_name == user_update_data["first_name"]

# Tests for UserResponse
def test_user_response_valid(user_response_data):
    user = UserResponse(**user_response_data)
    assert user.id == user_response_data["id"]

# Tests for LoginRequest
def test_login_request_valid(login_request_data):
    login = LoginRequest(**login_request_data)
    assert login.email == login_request_data["email"]
    assert login.password == login_request_data["password"]

# Parametrized tests for nickname and email validation
@pytest.mark.parametrize("nickname", ["dev_master", "web-pro", "dev123", "123coder"])
def test_user_base_nickname_valid(nickname, user_base_data):
    user_base_data["nickname"] = nickname
    user = UserBase(**user_base_data)
    assert user.nickname == nickname

@pytest.mark.parametrize("nickname", ["dev master", "web?coder", "", "de"])
def test_user_base_nickname_invalid(nickname, user_base_data):
    user_base_data["nickname"] = nickname
    with pytest.raises(ValidationError):
        UserBase(**user_base_data)

# Parametrized tests for URL validation
@pytest.mark.parametrize("url", ["http://valid.com/avatar.jpg", "https://valid.com/avatar.png", None])
def test_user_base_url_valid(url, user_base_data):
    user_base_data["profile_picture_url"] = url
    user = UserBase(**user_base_data)
    assert user.profile_picture_url == url

@pytest.mark.parametrize("url", ["ftp://invalid.com/avatar.jpg", "http//invalid", "https//invalid"])
def test_user_base_url_invalid(url, user_base_data):
    user_base_data["profile_picture_url"] = url
    with pytest.raises(ValidationError):
        UserBase(**user_base_data)

# Test for UserProfileUpdate (when none of the fields are provided)
def test_user_profile_update_no_field():
    with pytest.raises(ValueError, match="At least one field must be provided for profile update"):
        UserProfileUpdate()

# Test for UserProfileUpdate with valid fields
def test_user_profile_update_valid():
    update_data = {
        "first_name": "Emily",
        "last_name": "Brown",
        "bio": "Web designer and UX enthusiast",
        "profile_picture_url": "https://example.com/profile_pictures/emily.jpg"
    }
    user_profile_update = UserProfileUpdate(**update_data)
    assert user_profile_update.first_name == "Emily"
    assert user_profile_update.last_name == "Brown"
    assert user_profile_update.bio == "Web designer and UX enthusiast"
    assert user_profile_update.profile_picture_url == "https://example.com/profile_pictures/emily.jpg"

# Test for UserProfileUpdate with invalid URL
def test_user_profile_update_invalid_url():
    update_data = {
        "profile_picture_url": "invalid-url"
    }
    with pytest.raises(ValidationError):
        UserProfileUpdate(**update_data)

# Test for UserProfileUpdate with partial valid fields
def test_user_profile_update_partial_valid():
    update_data = {
        "bio": "Frontend specialist",
        "github_profile_url": "https://github.com/emilybrown"
    }
    user_profile_update = UserProfileUpdate(**update_data)
    assert user_profile_update.bio == "Frontend specialist"
    assert user_profile_update.github_profile_url == "https://github.com/emilybrown"