from builtins import bool, int, str
from datetime import datetime
from enum import Enum
import uuid
from sqlalchemy import (
    Column, String, Integer, DateTime, Boolean, func, Enum as SQLAlchemyEnum
)
from sqlalchemy.dialects.postgresql import UUID, ENUM
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base

class UserRole(Enum):
    """Enumeration of user roles within the application, stored as ENUM in the database."""
    ANONYMOUS = "ANONYMOUS"
    AUTHENTICATED = "AUTHENTICATED"
    MANAGER = "MANAGER"
    ADMIN = "ADMIN"

class User(Base):
    """
    Represents a user within the application, corresponding to the 'users' table in the database.
    This class uses SQLAlchemy ORM for mapping attributes to database columns efficiently.
    """
    __tablename__ = "users"
    __mapper_args__ = {"eager_defaults": True}

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nickname: Mapped[str] = Column(String(50), unique=True, nullable=False, index=True)
    email: Mapped[str] = Column(String(255), unique=True, nullable=False, index=True)
    first_name: Mapped[str] = Column(String(100), nullable=True)
    last_name: Mapped[str] = Column(String(100), nullable=True)
    bio: Mapped[str] = Column(String(500), nullable=True)
    profile_picture_url: Mapped[str] = Column(String(255), nullable=True)
    linkedin_profile_url: Mapped[str] = Column(String(255), nullable=True)
    github_profile_url: Mapped[str] = Column(String(255), nullable=True)
    role: Mapped[UserRole] = Column(
        SQLAlchemyEnum(UserRole, name='UserRole', create_constraint=True), 
        nullable=False, 
        default=UserRole.AUTHENTICATED  # Default role
    )
    is_professional: Mapped[bool] = Column(Boolean, default=False)
    professional_status_updated_at: Mapped[datetime] = Column(DateTime(timezone=True), nullable=True)
    last_login_at: Mapped[datetime] = Column(DateTime(timezone=True), nullable=True)
    failed_login_attempts: Mapped[int] = Column(Integer, default=0)
    is_locked: Mapped[bool] = Column(Boolean, default=False)
    created_at: Mapped[datetime] = Column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    verification_token = Column(String, nullable=True)
    email_verified: Mapped[bool] = Column(Boolean, default=False, nullable=False)
    hashed_password: Mapped[str] = Column(String(255), nullable=False)

    def __repr__(self) -> str:
        """Provides a readable representation of a user object."""
        return f"<User {self.nickname}, Role: {self.role.name}>"

    def lock_account(self):
        """Locks the user account."""
        self.is_locked = True

    def unlock_account(self):
        """Unlocks the user account."""
        self.is_locked = False

    def verify_email(self):
        """Marks the user's email as verified."""
        self.email_verified = True

    def has_role(self, role_name: UserRole) -> bool:
        """
        Checks if the user has a specified role.
        Args:
            role_name (UserRole): Role to check.
        Returns:
            bool: True if the user has the role, False otherwise.
        """
        return self.role == role_name

    def has_roles(self, *roles: UserRole) -> bool:
        """
        Checks if the user has one of the specified roles.
        Args:
            *roles (UserRole): Roles to check.
        Returns:
            bool: True if the user has one of the roles, False otherwise.
        """
        return self.role in roles

    def promote_role(self, new_role: UserRole):
        """
        Promotes the user to a new role.
        Args:
            new_role (UserRole): The role to promote the user to.
        """
        if not isinstance(new_role, UserRole):
            raise ValueError("Invalid role")
        self.role = new_role

    def demote_role(self, new_role: UserRole):
        """
        Demotes the user to a lower role.
        Args:
            new_role (UserRole): The role to demote the user to.
        """
        if not isinstance(new_role, UserRole):
            raise ValueError("Invalid role")
        self.role = new_role

    def update_professional_status(self, status: bool):
        """
        Updates the professional status and logs the update time.
        Args:
            status (bool): New professional status.
        """
        self.is_professional = status
        self.professional_status_updated_at = func.now()
