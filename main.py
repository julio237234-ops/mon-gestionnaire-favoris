from strawberry.asgi import GraphQL
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from schema import schema
from database import create_db_and_tables
import uvicorn
import os

app = FastAPI()

# Create the GraphQL ASGI app
graphql_app = GraphQL(schema)

# Mount GraphQL at /graphql
app.add_route("/graphql", graphql_app)
app.add_api_websocket_route("/graphql", graphql_app)

@app.get("/", response_class=HTMLResponse)
async def read_index():
    return """
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Gestionnaire de Favoris</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    </head>
    <body class="bg-gray-100 min-h-screen">
        <div class="container mx-auto px-4 py-8 max-w-4xl">
            <header class="mb-10 text-center">
                <h1 class="text-4xl font-bold text-blue-600 mb-2">Mes Favoris</h1>
                <p class="text-gray-600">Gérez vos liens importants simplement</p>
            </header>

            <!-- Formulaire d'ajout -->
            <div class="bg-white rounded-lg shadow-md p-6 mb-8">
                <h2 class="text-xl font-semibold mb-4 text-gray-800">Ajouter un nouveau favori</h2>
                <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <input type="text" id="name" placeholder="Nom du site" class="border rounded-md px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500">
                    <input type="url" id="url" placeholder="URL (https://...)" class="border rounded-md px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500">
                    <select id="category" class="border rounded-md px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500">
                        <option value="Général">Général</option>
                        <option value="Travail">Travail</option>
                        <option value="Loisirs">Loisirs</option>
                        <option value="Développement">Développement</option>
                        <option value="Recherche">Recherche</option>
                    </select>
                </div>
                <button onclick="addBookmark()" class="mt-4 w-full bg-blue-600 text-white font-bold py-2 px-4 rounded-md hover:bg-blue-700 transition duration-300">
                    <i class="fas fa-plus mr-2"></i> Ajouter
                </button>
            </div>

            <!-- Liste des favoris -->
            <div class="bg-white rounded-lg shadow-md overflow-hidden">
                <div class="bg-gray-50 px-6 py-4 border-b flex justify-between items-center">
                    <h2 class="text-xl font-semibold text-gray-800">Liste des favoris</h2>
                    <div class="flex items-center gap-2">
                        <span class="text-sm text-gray-500">Filtrer :</span>
                        <select onchange="fetchBookmarks(this.value)" id="filterCategory" class="text-sm border rounded-md px-2 py-1">
                            <option value="">Tous</option>
                            <option value="Général">Général</option>
                            <option value="Travail">Travail</option>
                            <option value="Loisirs">Loisirs</option>
                            <option value="Développement">Développement</option>
                            <option value="Recherche">Recherche</option>
                        </select>
                    </div>
                </div>
                <div id="bookmarksList" class="divide-y divide-gray-200">
                    <!-- Les favoris seront insérés ici -->
                    <div class="p-8 text-center text-gray-500 italic">Chargement des favoris...</div>
                </div>
            </div>
        </div>

        <script>
            const GRAPHQL_URL = '/graphql';

            async function gql(query, variables = {}) {
                const response = await fetch(GRAPHQL_URL, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ query, variables })
                });
                return response.json();
            }

            async function fetchBookmarks(category = "") {
                const query = `
                    query GetBookmarks($category: String) {
                        bookmarks(category: $category) {
                            id
                            name
                            url
                            category
                        }
                    }
                `;
                const result = await gql(query, { category: category || null });
                const list = document.getElementById('bookmarksList');
                
                if (result.data.bookmarks.length === 0) {
                    list.innerHTML = '<div class="p-8 text-center text-gray-500 italic">Aucun favori trouvé.</div>';
                    return;
                }

                list.innerHTML = result.data.bookmarks.map(b => `
                    <div class="flex items-center justify-between p-6 hover:bg-gray-50 transition">
                        <div class="flex-1">
                            <h3 class="font-bold text-gray-900 text-lg">${b.name}</h3>
                            <a href="${b.url}" target="_blank" class="text-blue-500 hover:underline text-sm break-all">${b.url}</a>
                            <div class="mt-1">
                                <span class="inline-block bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded-full font-semibold uppercase tracking-wide">${b.category}</span>
                            </div>
                        </div>
                        <div class="flex gap-2">
                            <button onclick="deleteBookmark(${b.id})" class="text-red-500 hover:text-red-700 p-2 transition">
                                <i class="fas fa-trash-alt"></i>
                            </button>
                        </div>
                    </div>
                `).join('');
            }

            async function addBookmark() {
                const name = document.getElementById('name').value;
                const url = document.getElementById('url').value;
                const category = document.getElementById('category').value;

                if (!name || !url) {
                    alert('Veuillez remplir le nom et l\\'URL');
                    return;
                }

                const mutation = `
                    mutation CreateBookmark($name: String!, $url: String!, $category: String!) {
                        createBookmark(name: $name, url: $url, category: $category) {
                            id
                        }
                    }
                `;
                
                await gql(mutation, { name, url, category });
                
                // Reset fields
                document.getElementById('name').value = '';
                document.getElementById('url').value = '';
                
                // Refresh list
                fetchBookmarks(document.getElementById('filterCategory').value);
            }

            async function deleteBookmark(id) {
                if (!confirm('Voulez-vous vraiment supprimer ce favori ?')) return;

                const mutation = `
                    mutation DeleteBookmark($id: Int!) {
                        deleteBookmark(id: $id)
                    }
                `;
                await gql(mutation, { id });
                fetchBookmarks(document.getElementById('filterCategory').value);
            }

            // Initial load
            fetchBookmarks();
        </script>
    </body>
    </html>
    """

def init_db():
    create_db_and_tables()

if __name__ == "__main__":
    init_db()
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)