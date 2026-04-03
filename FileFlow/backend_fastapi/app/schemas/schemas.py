from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, ConfigDict


# User schemas
class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(..., min_length=6, max_length=100)


class UserLogin(BaseModel):
    username: str
    password: str


class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


# Token schemas
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: int | None = None
    username: str | None = None


class RefreshToken(BaseModel):
    refresh_token: str


# File schemas
class FileBase(BaseModel):
    filename: str = Field(..., min_length=1, max_length=255)


class FileCreate(FileBase):
    parent_folder_id: int | None = None
    is_folder: bool = False


class FileUpdate(BaseModel):
    filename: str | None = None
    is_favorite: bool | None = None
    tags: str | None = None


class FileMove(BaseModel):
    destination_folder_id: int | None = None


class FileRename(BaseModel):
    new_name: str = Field(..., min_length=1, max_length=255)


class FileResponse(FileBase):
    id: int
    filepath: str
    is_folder: bool
    parent_folder_id: int | None
    created_at: datetime
    modified_at: datetime
    filesize: int
    mimetype: str | None
    is_favorite: bool
    tags: list[str] = []
    
    model_config = ConfigDict(from_attributes=True)
    
    @classmethod
    def from_orm_with_tags(cls, obj):
        """Convert ORM object to response with tags as list"""
        data = {
            "id": obj.id,
            "filename": obj.filename,
            "filepath": obj.filepath,
            "is_folder": obj.is_folder,
            "parent_folder_id": obj.parent_folder_id,
            "created_at": obj.created_at,
            "modified_at": obj.modified_at,
            "filesize": obj.filesize,
            "mimetype": obj.mimetype,
            "is_favorite": obj.is_favorite,
            "tags": obj.tags.split(",") if obj.tags else []
        }
        return cls(**data)


# Folder schemas
class FolderCreate(BaseModel):
    folder_name: str = Field(..., min_length=1, max_length=255)
    parent_folder_id: int | None = None


class BreadcrumbItem(BaseModel):
    id: int
    name: str


class FolderContents(BaseModel):
    files: list[FileResponse]
    breadcrumbs: list[BreadcrumbItem]
    current_folder_id: int | None


# Search schemas
class SearchRequest(BaseModel):
    query: str | None = None
    file_types: list[str] = []
    size_min: int | None = None
    size_max: int | None = None
    date_from: datetime | None = None
    date_to: datetime | None = None


class SearchProfileCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    query: str | None = None
    file_types: list[str] = []
    size_min: int | None = None
    size_max: int | None = None
    date_from: datetime | None = None
    date_to: datetime | None = None


class SearchProfileResponse(SearchProfileCreate):
    id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


# Compression schemas
class CompressionCreate(BaseModel):
    file_ids: list[int] = Field(..., min_length=1)
    archive_name: str = Field(default="archive", min_length=1, max_length=100)
    format: str = Field(default="zip", pattern="^(zip|tar|tar\\.gz|tar\\.bz2|7z)$")
    password: str | None = None


class CompressionExtract(BaseModel):
    password: str | None = None


# Generic response schemas
class MessageResponse(BaseModel):
    message: str


class SuccessResponse(BaseModel):
    success: bool
    message: str | None = None


class ErrorResponse(BaseModel):
    detail: str
