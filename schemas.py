"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List

# Portfolio-specific schemas

class Profile(BaseModel):
    """
    Personal profile for the portfolio owner
    Collection name: "profile"
    """
    name: str = Field(..., description="Your full name")
    title: str = Field(..., description="Headline or current role")
    summary: str = Field(..., description="Short bio / about you")
    location: Optional[str] = Field(None, description="Where you're based")
    email: Optional[str] = Field(None, description="Contact email")
    website: Optional[HttpUrl] = Field(None, description="Personal website")
    github: Optional[HttpUrl] = Field(None, description="GitHub profile")
    linkedin: Optional[HttpUrl] = Field(None, description="LinkedIn profile")
    skills: List[str] = Field(default_factory=list, description="Key skills")

class Project(BaseModel):
    """
    Portfolio projects
    Collection name: "project"
    """
    title: str = Field(..., description="Project name")
    description: str = Field(..., description="What the project does")
    purpose: Optional[str] = Field(None, description="Why you built it / impact")
    languages: List[str] = Field(default_factory=list, description="Programming languages used")
    frameworks: List[str] = Field(default_factory=list, description="Frameworks/libraries used")
    timeframe: Optional[str] = Field(None, description="When you built it (e.g., 2024 Q1)")
    repo_url: Optional[HttpUrl] = Field(None, description="Git repository URL")
    live_url: Optional[HttpUrl] = Field(None, description="Live demo URL")
    highlights: List[str] = Field(default_factory=list, description="Bullet points of achievements")

# Example schemas (kept for reference but not used by the app)
class User(BaseModel):
    name: str
    email: str
    address: str
    age: Optional[int] = None
    is_active: bool = True

class Product(BaseModel):
    title: str
    description: Optional[str] = None
    price: float
    category: str
    in_stock: bool = True

# Note: The Flames database viewer can inspect these schemas via /schema
