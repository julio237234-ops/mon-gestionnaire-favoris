import pytest
from fastapi.testclient import TestClient
from main import app, API_KEY
import json

client = TestClient(app)

def test_graphql_unauthorized():
    """Vérifie que l'accès sans clé API est refusé."""
    query = "{ bookmarks { id name } }"
    response = client.post("/graphql", json={"query": query})
    assert response.status_code == 403

def test_create_bookmark():
    """Teste la création d'un favori avec clé API."""
    mutation = """
        mutation {
            createBookmark(name: "Test Site", url: "https://test.com", category: "Travail") {
                id
                name
                url
                category
            }
        }
    """
    response = client.post(
        "/graphql", 
        json={"query": mutation},
        headers={"X-API-KEY": API_KEY}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["createBookmark"]["name"] == "Test Site"
    return data["data"]["createBookmark"]["id"]

def test_fetch_bookmarks():
    """Teste la récupération avec filtrage et recherche."""
    query = """
        query {
            bookmarks(search: "Test") {
                name
            }
        }
    """
    response = client.post(
        "/graphql", 
        json={"query": query},
        headers={"X-API-KEY": API_KEY}
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data["data"]["bookmarks"]) > 0

def test_invalid_url():
    """Vérifie que le backend rejette les URLs invalides."""
    mutation = """
        mutation {
            createBookmark(name: "Bad URL", url: "not-a-url") {
                id
            }
        }
    """
    response = client.post(
        "/graphql", 
        json={"query": mutation},
        headers={"X-API-KEY": API_KEY}
    )
    assert "errors" in response.json()
