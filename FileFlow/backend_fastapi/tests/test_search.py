import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_search_empty(client: AsyncClient, auth_headers):
    """Test search with no results"""
    response = await client.post(
        "/api/search",
        headers=auth_headers,
        json={"query": "nonexistent"}
    )
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_search_by_name(client: AsyncClient, auth_headers):
    """Test search by filename"""
    # Create test folders
    await client.post(
        "/api/folders",
        headers=auth_headers,
        json={"folder_name": "searchable folder"}
    )
    await client.post(
        "/api/folders",
        headers=auth_headers,
        json={"folder_name": "other folder"}
    )
    
    # Search
    response = await client.post(
        "/api/search",
        headers=auth_headers,
        json={"query": "searchable"}
    )
    assert response.status_code == 200
    results = response.json()
    assert len(results) == 1
    assert results[0]["filename"] == "searchable folder"


@pytest.mark.asyncio
async def test_create_search_profile(client: AsyncClient, auth_headers):
    """Test creating a search profile"""
    response = await client.post(
        "/api/search/profiles",
        headers=auth_headers,
        json={
            "name": "My Search",
            "query": "documents",
            "file_types": ["application/pdf"]
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "My Search"
    assert data["query"] == "documents"


@pytest.mark.asyncio
async def test_get_search_profiles(client: AsyncClient, auth_headers):
    """Test listing search profiles"""
    # Create a profile first
    await client.post(
        "/api/search/profiles",
        headers=auth_headers,
        json={"name": "Test Profile", "query": "test"}
    )
    
    # List profiles
    response = await client.get("/api/search/profiles", headers=auth_headers)
    assert response.status_code == 200
    profiles = response.json()
    assert len(profiles) >= 1
    assert any(p["name"] == "Test Profile" for p in profiles)


@pytest.mark.asyncio
async def test_delete_search_profile(client: AsyncClient, auth_headers):
    """Test deleting a search profile"""
    # Create a profile
    create_response = await client.post(
        "/api/search/profiles",
        headers=auth_headers,
        json={"name": "To Delete", "query": "delete"}
    )
    profile_id = create_response.json()["id"]
    
    # Delete it
    response = await client.delete(f"/api/search/profiles/{profile_id}", headers=auth_headers)
    assert response.status_code == 200
    
    # Verify it's gone
    list_response = await client.get("/api/search/profiles", headers=auth_headers)
    profiles = list_response.json()
    assert not any(p["id"] == profile_id for p in profiles)
