from fastapi import APIRouter, HTTPException, status, UploadFile, File as FastAPIFile
from fastapi.responses import StreamingResponse, FileResponse
from sqlalchemy import select
from pathlib import Path
from app.models import File, get_db
from app.schemas import FileResponse as FileResponseSchema, FileRename, FileMove, SuccessResponse
from app.services import CurrentUser, DbSession, file_service
from app.utils import Validators, get_mimetype
from app.config import get_settings

settings = get_settings()
router = APIRouter(prefix="/api/files", tags=["Files"])


@router.get("", response_model=list[FileResponseSchema])
async def list_files(
    current_user: CurrentUser,
    db: DbSession,
    folder_id: int | None = None
):
    """List files in a folder (or root if folder_id is None)"""
    query = select(File).where(
        File.user_id == current_user.id,
        File.parent_folder_id == folder_id
    ).order_by(File.is_folder.desc(), File.filename)
    
    result = await db.execute(query)
    files = result.scalars().all()
    
    return [FileResponseSchema.from_orm_with_tags(f) for f in files]


@router.post("/upload", response_model=FileResponseSchema, status_code=status.HTTP_201_CREATED)
async def upload_file(
    current_user: CurrentUser,
    db: DbSession,
    file: UploadFile = FastAPIFile(...),
    folder_id: int | None = None
):
    """Upload a file"""
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No filename provided"
        )
    
    # Validate file extension
    if not Validators.allowed_file(file.filename, settings.allowed_extensions):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type not allowed. Allowed: {', '.join(settings.allowed_extensions)}"
        )
    
    # Validate folder if provided
    if folder_id:
        result = await db.execute(
            select(File).where(
                File.id == folder_id,
                File.user_id == current_user.id,
                File.is_folder == True
            )
        )
        if not result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Folder not found"
            )
    
    # Sanitize filename
    safe_filename = Validators.sanitize_filename(file.filename)
    
    # Save file
    file_info = await file_service.save_file(
        file.file,
        safe_filename,
        current_user.id
    )
    
    # Create database record
    new_file = File(
        filename=file_info['filename'],
        filepath=file_info['filepath'],
        user_id=current_user.id,
        parent_folder_id=folder_id,
        filesize=file_info['size'],
        mimetype=file_info['mimetype'],
        file_hash=file_info['file_hash']
    )
    db.add(new_file)
    await db.commit()
    await db.refresh(new_file)
    
    return FileResponseSchema.from_orm_with_tags(new_file)


@router.get("/download/{file_id}")
async def download_file(file_id: int, current_user: CurrentUser, db: DbSession):
    """Download a file"""
    result = await db.execute(
        select(File).where(File.id == file_id, File.user_id == current_user.id)
    )
    file = result.scalar_one_or_none()
    
    if not file:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")
    
    if file.is_folder:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot download a folder")
    
    if not Path(file.filepath).exists():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found in storage")
    
    return FileResponse(
        path=file.filepath,
        filename=file.filename,
        media_type=file.mimetype or "application/octet-stream"
    )


@router.get("/view/{file_id}")
async def view_file(file_id: int, current_user: CurrentUser, db: DbSession):
    """View a file (inline)"""
    result = await db.execute(
        select(File).where(File.id == file_id, File.user_id == current_user.id)
    )
    file = result.scalar_one_or_none()
    
    if not file:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")
    
    if file.is_folder:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot view a folder")
    
    filepath = Path(file.filepath)
    if not filepath.exists():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found in storage")
    
    return StreamingResponse(
        file_service.read_file_chunks(str(filepath)),
        media_type=file.mimetype or "application/octet-stream"
    )


@router.delete("/{file_id}", response_model=SuccessResponse)
async def delete_file(file_id: int, current_user: CurrentUser, db: DbSession):
    """Delete a file or folder"""
    result = await db.execute(
        select(File).where(File.id == file_id, File.user_id == current_user.id)
    )
    file = result.scalar_one_or_none()
    
    if not file:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")
    
    if file.is_folder:
        # Recursively delete folder contents
        await _delete_folder_contents(db, file.id, current_user.id)
    else:
        # Delete physical file
        await file_service.delete_file(file.filepath)
    
    await db.delete(file)
    await db.commit()
    
    return SuccessResponse(success=True, message="File deleted successfully")


async def _delete_folder_contents(db: DbSession, folder_id: int, user_id: int):
    """Recursively delete folder contents"""
    result = await db.execute(
        select(File).where(File.parent_folder_id == folder_id, File.user_id == user_id)
    )
    contents = result.scalars().all()
    
    for item in contents:
        if item.is_folder:
            await _delete_folder_contents(db, item.id, user_id)
        else:
            await file_service.delete_file(item.filepath)
        await db.delete(item)


@router.post("/{file_id}/rename", response_model=FileResponseSchema)
async def rename_file(
    file_id: int,
    rename_data: FileRename,
    current_user: CurrentUser,
    db: DbSession
):
    """Rename a file"""
    result = await db.execute(
        select(File).where(File.id == file_id, File.user_id == current_user.id)
    )
    file = result.scalar_one_or_none()
    
    if not file:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")
    
    if not Validators.is_valid_filename(rename_data.new_name):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid filename")
    
    file.filename = Validators.sanitize_filename(rename_data.new_name)
    await db.commit()
    await db.refresh(file)
    
    return FileResponseSchema.from_orm_with_tags(file)


@router.post("/{file_id}/move", response_model=FileResponseSchema)
async def move_file(
    file_id: int,
    move_data: FileMove,
    current_user: CurrentUser,
    db: DbSession
):
    """Move a file to a different folder"""
    result = await db.execute(
        select(File).where(File.id == file_id, File.user_id == current_user.id)
    )
    file = result.scalar_one_or_none()
    
    if not file:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")
    
    # Validate destination folder
    if move_data.destination_folder_id is not None:
        result = await db.execute(
            select(File).where(
                File.id == move_data.destination_folder_id,
                File.user_id == current_user.id,
                File.is_folder == True
            )
        )
        if not result.scalar_one_or_none():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid destination folder")
    
    file.parent_folder_id = move_data.destination_folder_id
    await db.commit()
    await db.refresh(file)
    
    return FileResponseSchema.from_orm_with_tags(file)


@router.post("/{file_id}/favorite", response_model=FileResponseSchema)
async def toggle_favorite(file_id: int, current_user: CurrentUser, db: DbSession):
    """Toggle favorite status of a file"""
    result = await db.execute(
        select(File).where(File.id == file_id, File.user_id == current_user.id)
    )
    file = result.scalar_one_or_none()
    
    if not file:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")
    
    file.is_favorite = not file.is_favorite
    await db.commit()
    await db.refresh(file)
    
    return FileResponseSchema.from_orm_with_tags(file)
