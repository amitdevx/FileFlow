from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select, or_
from datetime import datetime
from app.models import File, SearchProfile, get_db
from app.schemas import (
    SearchRequest, SearchProfileCreate, SearchProfileResponse,
    FileResponse, SuccessResponse
)
from app.services import CurrentUser, DbSession

router = APIRouter(prefix="/api/search", tags=["Search"])


@router.post("", response_model=list[FileResponse])
async def search_files(
    search_data: SearchRequest,
    current_user: CurrentUser,
    db: DbSession
):
    """Advanced file search"""
    query = select(File).where(File.user_id == current_user.id)
    
    # Text search (filename and tags)
    if search_data.query:
        search_term = f"%{search_data.query}%"
        query = query.where(
            or_(
                File.filename.ilike(search_term),
                File.tags.ilike(search_term)
            )
        )
    
    # File type filter
    if search_data.file_types:
        type_conditions = [File.mimetype.ilike(f"{ft}%") for ft in search_data.file_types]
        query = query.where(or_(*type_conditions))
    
    # Size filters
    if search_data.size_min is not None:
        query = query.where(File.filesize >= search_data.size_min)
    if search_data.size_max is not None:
        query = query.where(File.filesize <= search_data.size_max)
    
    # Date filters
    if search_data.date_from:
        query = query.where(File.created_at >= search_data.date_from)
    if search_data.date_to:
        query = query.where(File.created_at <= search_data.date_to)
    
    result = await db.execute(query)
    files = result.scalars().all()
    
    return [FileResponse.from_orm_with_tags(f) for f in files]


@router.get("/profiles", response_model=list[SearchProfileResponse])
async def get_search_profiles(current_user: CurrentUser, db: DbSession):
    """Get saved search profiles"""
    result = await db.execute(
        select(SearchProfile).where(SearchProfile.user_id == current_user.id)
    )
    profiles = result.scalars().all()
    
    return [
        SearchProfileResponse(
            id=p.id,
            name=p.name,
            query=p.query,
            file_types=p.file_types.split(',') if p.file_types else [],
            size_min=p.size_min,
            size_max=p.size_max,
            date_from=p.date_from,
            date_to=p.date_to,
            created_at=p.created_at
        )
        for p in profiles
    ]


@router.post("/profiles", response_model=SearchProfileResponse, status_code=status.HTTP_201_CREATED)
async def create_search_profile(
    profile_data: SearchProfileCreate,
    current_user: CurrentUser,
    db: DbSession
):
    """Save a search profile"""
    profile = SearchProfile(
        name=profile_data.name,
        user_id=current_user.id,
        query=profile_data.query,
        file_types=','.join(profile_data.file_types) if profile_data.file_types else None,
        size_min=profile_data.size_min,
        size_max=profile_data.size_max,
        date_from=profile_data.date_from,
        date_to=profile_data.date_to
    )
    db.add(profile)
    await db.commit()
    await db.refresh(profile)
    
    return SearchProfileResponse(
        id=profile.id,
        name=profile.name,
        query=profile.query,
        file_types=profile.file_types.split(',') if profile.file_types else [],
        size_min=profile.size_min,
        size_max=profile.size_max,
        date_from=profile.date_from,
        date_to=profile.date_to,
        created_at=profile.created_at
    )


@router.delete("/profiles/{profile_id}", response_model=SuccessResponse)
async def delete_search_profile(
    profile_id: int,
    current_user: CurrentUser,
    db: DbSession
):
    """Delete a search profile"""
    result = await db.execute(
        select(SearchProfile).where(
            SearchProfile.id == profile_id,
            SearchProfile.user_id == current_user.id
        )
    )
    profile = result.scalar_one_or_none()
    
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Search profile not found"
        )
    
    await db.delete(profile)
    await db.commit()
    
    return SuccessResponse(success=True, message="Profile deleted successfully")
