import requests
import json

url = "http://localhost:8000/graphql"

# Get all tasks
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
print("All Tasks:", json.dumps(response.json(), indent=2))

# Mark task as complete
mutation = """
mutation {
    updateTask(id: 2, completed: true) {
        id
        title
        completed
    }
}
"""
response = requests.post(url, json={'query': mutation})
print("\nComplete Task:", json.dumps(response.json(), indent=2))

# Delete task
mutation = """
mutation {
    deleteTask(id: 2) {
        success
    }
}
"""
response = requests.post(url, json={'query': mutation})
print("\nDelete Task:", json.dumps(response.json(), indent=2))

# Get all tasks again
response = requests.post(url, json={'query': query})
print("\nAll Tasks After Delete:", json.dumps(response.json(), indent=2))