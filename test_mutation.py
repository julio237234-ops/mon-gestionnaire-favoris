import requests
import json

url = "http://localhost:8000/graphql"

# Mutation to create a task
mutation = """
mutation {
    createTask(title: "Test task", description: "This is a test") {
        id
        title
        description
        completed
    }
}
"""

response = requests.post(url, json={'query': mutation})
print("Status code:", response.status_code)
print("Response:", json.dumps(response.json(), indent=2))