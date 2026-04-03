import pytest
from httpx import AsyncClient
import io


@pytest.mark.asyncio
async def test_list_files_empty(client: AsyncClient, auth_headers):
    """Test listing files when none exist"""
    response = await client.get("/api/files", headers=auth_headers)
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_create_folder(client: AsyncClient, auth_headers):
    """Test creating a folder"""
    response = await client.post(
        "/api/folders",
        headers=auth_headers,
        json={"folder_name": "Test Folder"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["filename"] == "Test Folder"
    assert data["is_folder"] == True


@pytest.mark.asyncio
async def test_create_folder_duplicate_name(client: AsyncClient, auth_headers):
    """Test creating folder with duplicate name"""
    # Create first folder
    await client.post(
        "/api/folders",
        headers=auth_headers,
        json={"folder_name": "Duplicate Folder"}
    )
    
    # Try to create duplicate
    response = await client.post(
        "/api/folders",
        headers=auth_headers,
        json={"folder_name": "Duplicate Folder"}
    )
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_list_folder_contents(client: AsyncClient, auth_headers):
    """Test listing folder contents"""
    # Create a folder
    create_response = await client.post(
        "/api/folders",
        headers=auth_headers,
        json={"folder_name": "Parent Folder"}
    )
    folder_id = create_response.json()["id"]
    
    # Get folder contents
    response = await client.get(f"/api/folders/{folder_id}", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert "files" in data
    assert "breadcrumbs" in data


@pytest.mark.asyncio
async def test_delete_folder(client: AsyncClient, auth_headers):
    """Test deleting a folder"""
    # Create a folder
    create_response = await client.post(
        "/api/folders",
        headers=auth_headers,
        json={"folder_name": "To Delete"}
    )
    folder_id = create_response.json()["id"]
    
    # Delete the folder
    response = await client.delete(f"/api/folders/{folder_id}", headers=auth_headers)
    assert response.status_code == 200
    
    # Verify it's gone
    response = await client.get(f"/api/folders/{folder_id}", headers=auth_headers)
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_rename_file(client: AsyncClient, auth_headers):
    """Test renaming a folder"""
    # Create a folder
    create_response = await client.post(
        "/api/folders",
        headers=auth_headers,
        json={"folder_name": "Original Name"}
    )
    file_id = create_response.json()["id"]
    
    # Rename it
    response = await client.post(
        f"/api/files/{file_id}/rename",
        headers=auth_headers,
        json={"new_name": "New Name"}
    )
    assert response.status_code == 200
    assert response.json()["filename"] == "New Name"


@pytest.mark.asyncio
async def test_move_file(client: AsyncClient, auth_headers):
    """Test moving a file to another folder"""
    # Create destination folder
    dest_response = await client.post(
        "/api/folders",
        headers=auth_headers,
        json={"folder_name": "Destination"}
    )
    dest_id = dest_response.json()["id"]
    
    # Create file to move
    file_response = await client.post(
        "/api/folders",
        headers=auth_headers,
        json={"folder_name": "To Move"}
    )
    file_id = file_response.json()["id"]
    
    # Move file
    response = await client.post(
        f"/api/files/{file_id}/move",
        headers=auth_headers,
        json={"destination_folder_id": dest_id}
    )
    assert response.status_code == 200
    assert response.json()["parent_folder_id"] == dest_id


@pytest.mark.asyncio
async def test_toggle_favorite(client: AsyncClient, auth_headers):
    """Test toggling favorite status"""
    # Create a folder
    create_response = await client.post(
        "/api/folders",
        headers=auth_headers,
        json={"folder_name": "Favorite Test"}
    )
    file_id = create_response.json()["id"]
    
    # Toggle favorite (should be true)
    response = await client.post(f"/api/files/{file_id}/favorite", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["is_favorite"] == True
    
    # Toggle again (should be false)
    response = await client.post(f"/api/files/{file_id}/favorite", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["is_favorite"] == False
