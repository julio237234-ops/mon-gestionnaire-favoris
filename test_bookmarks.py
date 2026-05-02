import requests

def test_bookmarks():
    url = "http://localhost:8000"
    
    # 1. Créer un favori
    create_mutation = """
    mutation {
      createBookmark(name: "Google", url: "https://www.google.com", category: "Recherche") {
        id
        name
        url
        category
      }
    }
    """
    response = requests.post(url, json={'query': create_mutation})
    print("Création:", response.json())
    
    # 2. Créer un autre favori
    create_mutation_2 = """
    mutation {
      createBookmark(name: "GitHub", url: "https://github.com", category: "Développement") {
        id
        name
      }
    }
    """
    requests.post(url, json={'query': create_mutation_2})
    
    # 3. Lister les favoris
    query = """
    query {
      bookmarks {
        id
        name
        category
      }
    }
    """
    response = requests.post(url, json={'query': query})
    print("Liste complète:", response.json())
    
    # 4. Filtrer par catégorie
    filter_query = """
    query {
      bookmarks(category: "Développement") {
        name
      }
    }
    """
    response = requests.post(url, json={'query': filter_query})
    print("Filtre 'Développement':", response.json())

if __name__ == "__main__":
    try:
        test_bookmarks()
    except Exception as e:
        print(f"Erreur: {e}")
