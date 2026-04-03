from fastapi import APIRouter, HTTPException, status, BackgroundTasks
from sqlalchemy import select
from pathlib import Path
from app.models import File, get_db
from app.schemas import CompressionCreate, CompressionExtract, FileResponse, SuccessResponse
from app.services import CurrentUser, DbSession, compression_service
from app.config import get_settings

settings = get_settings()
router = APIRouter(prefix="/api/compress", tags=["Compression"])


@router.post("/create", response_model=FileResponse, status_code=status.HTTP_201_CREATED)
async def create_archive(
    compression_data: CompressionCreate,
    current_user: CurrentUser,
    db: DbSession,
    background_tasks: BackgroundTasks
):
    """Create a compressed archive"""
    # Get files
    result = await db.execute(
        select(File).where(
            File.id.in_(compression_data.file_ids),
            File.user_id == current_user.id
        )
    )
    files = result.scalars().all()
    
    file_paths = [f.filepath for f in files if not f.is_folder and Path(f.filepath).exists()]
    
    if not file_paths:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No valid files selected"
        )
    
    # Create output path
    output_dir = Path(settings.upload_folder) / str(current_user.id)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    format_type = compression_data.format
    output_path = output_dir / f"{compression_data.archive_name}.{format_type.replace('.', '_')}"
    
    # Handle duplicate names
    counter = 1
    original_stem = output_path.stem
    while output_path.exists():
        output_path = output_dir / f"{original_stem}_{counter}.{format_type.replace('.', '_')}"
        counter += 1
    
    # Create archive
    try:
        if format_type == 'zip':
            compression_service.create_zip(file_paths, str(output_path), compression_data.password)
            mimetype = 'application/zip'
        elif format_type in ['tar', 'tar.gz', 'tar.bz2']:
            compression = format_type.split('.')[-1] if '.' in format_type else None
            compression_service.create_tar(file_paths, str(output_path), compression)
            mimetype = 'application/x-tar'
        elif format_type == '7z':
            compression_service.create_7z(file_paths, str(output_path), compression_data.password)
            mimetype = 'application/x-7z-compressed'
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unsupported archive format"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create archive: {str(e)}"
        )
    
    # Add to database
    new_file = File(
        filename=output_path.name,
        filepath=str(output_path),
        user_id=current_user.id,
        filesize=output_path.stat().st_size,
        mimetype=mimetype
    )
    db.add(new_file)
    await db.commit()
    await db.refresh(new_file)
    
    return FileResponse.from_orm_with_tags(new_file)


@router.post("/extract/{file_id}", response_model=FileResponse)
async def extract_archive(
    file_id: int,
    extract_data: CompressionExtract,
    current_user: CurrentUser,
    db: DbSession
):
    """Extract a compressed archive"""
    result = await db.execute(
        select(File).where(File.id == file_id, File.user_id == current_user.id)
    )
    file = result.scalar_one_or_none()
    
    if not file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Archive not found"
        )
    
    if not Path(file.filepath).exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Archive file not found in storage"
        )
    
    # Create extraction directory
    extract_dir = Path(file.filepath).parent / Path(file.filepath).stem
    extract_dir.mkdir(parents=True, exist_ok=True)
    
    try:
        ext = Path(file.filepath).suffix.lower()
        
        if ext == '.zip':
            compression_service.extract_zip(file.filepath, str(extract_dir), extract_data.password)
        elif ext in ['.tar', '.gz', '.bz2', '.xz']:
            compression_service.extract_tar(file.filepath, str(extract_dir))
        elif ext == '.7z':
            compression_service.extract_7z(file.filepath, str(extract_dir), extract_data.password)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unsupported archive format"
            )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to extract archive: {str(e)}"
        )
    
    # Add extracted folder to database
    folder = File(
        filename=Path(file.filepath).stem,
        filepath=str(extract_dir),
        user_id=current_user.id,
        is_folder=True,
        parent_folder_id=file.parent_folder_id
    )
    db.add(folder)
    await db.commit()
    await db.refresh(folder)
    
    return FileResponse.from_orm_with_tags(folder)


@router.get("/list/{file_id}")
async def list_archive_contents(
    file_id: int,
    current_user: CurrentUser,
    db: DbSession
):
    """List contents of an archive"""
    result = await db.execute(
        select(File).where(File.id == file_id, File.user_id == current_user.id)
    )
    file = result.scalar_one_or_none()
    
    if not file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Archive not found"
        )
    
    if not Path(file.filepath).exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Archive file not found in storage"
        )
    
    try:
        contents = compression_service.list_archive_contents(file.filepath)
        return {"success": True, "contents": contents}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list archive contents: {str(e)}"
        )
