# Test create task
def test_create_task(client):
    # Create a new task
    response = client.post(
        "/tasks",
        json={
            "title": "Learn Docker"
        }
    )
    assert response.status_code == 201
    data = response.get_json()
    assert data["title"] == "Learn Docker"

# Test get all tasks
def test_get_tasks(client):
    # Create a task
    client.post(
        "/tasks",
        json={
            "title": "Learn Docker"
        }
    )
    # Get all tasks
    response = client.get("/tasks")
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) >= 1

# Test get task by ID
def test_get_task(client):
    # Create a task
    response = client.post(
        "/tasks",
        json={
            "title": "Learn Kubernetes"
        }
    )
    task = response.get_json()
    # Get task by ID
    response = client.get(f"/tasks/{task['id']}")
    assert response.status_code == 200
    data = response.get_json()
    assert data["title"] == "Learn Kubernetes"

# Test update task
def test_update_task(client):
    # Create a task
    response = client.post(
        "/tasks",
        json={
            "title": "Old Title"
        }
    )
    task = response.get_json()
    # Update task
    response = client.put(
        f"/tasks/{task['id']}",
        json={
            "title": "New Title"
        }
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["title"] == "New Title"

# Test delete task
def test_delete_task(client):
    # Create a task
    response = client.post(
        "/tasks",
        json={
            "title": "Delete Me"
        }
    )
    task = response.get_json()
    # Delete task
    response = client.delete(f"/tasks/{task['id']}")
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Task deleted"