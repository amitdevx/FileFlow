from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select
from app.models import File, get_db
from app.schemas import FolderCreate, FolderContents, FileResponse, BreadcrumbItem, SuccessResponse
from app.services import CurrentUser, DbSession

router = APIRouter(prefix="/api/folders", tags=["Folders"])


@router.get("", response_model=FolderContents)
async def get_folder_contents(
    current_user: CurrentUser,
    db: DbSession,
    folder_id: int | None = None
):
    """Get folder contents with breadcrumbs"""
    # Get files in folder
    query = select(File).where(
        File.user_id == current_user.id,
        File.parent_folder_id == folder_id
    ).order_by(File.is_folder.desc(), File.filename)
    
    result = await db.execute(query)
    files = result.scalars().all()
    
    # Build breadcrumbs
    breadcrumbs = []
    if folder_id:
        result = await db.execute(select(File).where(File.id == folder_id))
        current_folder = result.scalar_one_or_none()
        
        folder = current_folder
        while folder:
            breadcrumbs.insert(0, BreadcrumbItem(id=folder.id, name=folder.filename))
            if folder.parent_folder_id:
                result = await db.execute(select(File).where(File.id == folder.parent_folder_id))
                folder = result.scalar_one_or_none()
            else:
                folder = None
    
    return FolderContents(
        files=[FileResponse.from_orm_with_tags(f) for f in files],
        breadcrumbs=breadcrumbs,
        current_folder_id=folder_id
    )


@router.post("", response_model=FileResponse, status_code=status.HTTP_201_CREATED)
async def create_folder(
    folder_data: FolderCreate,
    current_user: CurrentUser,
    db: DbSession
):
    """Create a new folder"""
    # Validate parent folder if provided
    if folder_data.parent_folder_id:
        result = await db.execute(
            select(File).where(
                File.id == folder_data.parent_folder_id,
                File.user_id == current_user.id,
                File.is_folder == True
            )
        )
        if not result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Parent folder not found"
            )
    
    # Check for duplicate folder name in same location
    result = await db.execute(
        select(File).where(
            File.filename == folder_data.folder_name,
            File.user_id == current_user.id,
            File.parent_folder_id == folder_data.parent_folder_id,
            File.is_folder == True
        )
    )
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Folder with this name already exists"
        )
    
    new_folder = File(
        filename=folder_data.folder_name,
        filepath="",
        user_id=current_user.id,
        is_folder=True,
        parent_folder_id=folder_data.parent_folder_id
    )
    db.add(new_folder)
    await db.commit()
    await db.refresh(new_folder)
    
    return FileResponse.from_orm_with_tags(new_folder)


@router.get("/{folder_id}", response_model=FolderContents)
async def open_folder(
    folder_id: int,
    current_user: CurrentUser,
    db: DbSession
):
    """Open a folder and get its contents"""
    # Verify folder exists and belongs to user
    result = await db.execute(
        select(File).where(
            File.id == folder_id,
            File.user_id == current_user.id,
            File.is_folder == True
        )
    )
    folder = result.scalar_one_or_none()
    
    if not folder:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Folder not found"
        )
    
    return await get_folder_contents(current_user, db, folder_id)


@router.delete("/{folder_id}", response_model=SuccessResponse)
async def delete_folder(
    folder_id: int,
    current_user: CurrentUser,
    db: DbSession
):
    """Delete a folder and all its contents"""
    result = await db.execute(
        select(File).where(
            File.id == folder_id,
            File.user_id == current_user.id,
            File.is_folder == True
        )
    )
    folder = result.scalar_one_or_none()
    
    if not folder:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Folder not found"
        )
    
    # Recursively delete contents
    await _delete_folder_recursive(db, folder_id, current_user.id)
    
    await db.delete(folder)
    await db.commit()
    
    return SuccessResponse(success=True, message="Folder deleted successfully")


async def _delete_folder_recursive(db: DbSession, folder_id: int, user_id: int):
    """Recursively delete folder contents"""
    from app.services import file_service
    
    result = await db.execute(
        select(File).where(
            File.parent_folder_id == folder_id,
            File.user_id == user_id
        )
    )
    contents = result.scalars().all()
    
    for item in contents:
        if item.is_folder:
            await _delete_folder_recursive(db, item.id, user_id)
        else:
            await file_service.delete_file(item.filepath)
        await db.delete(item)
