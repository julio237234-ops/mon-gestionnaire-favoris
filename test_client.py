import requests
import json

url = "http://localhost:8000/graphql"

# Test a simple query to get all tasks (should be empty initially)
query = """
{
    tasks {
        id
        title
        description
        completed
    }
}
"""

response = requests.post(url, json={'query': query})
print("Status code:", response.status_code)
print("Response:", json.dumps(response.json(), indent=2))