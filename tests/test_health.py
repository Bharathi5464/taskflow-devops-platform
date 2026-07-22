# Test the /health endpoint
def test_health_endpoint(client):
    # Send a GET request to the /health endpoint
    response = client.get("/health")
    # Verify that the HTTP status code is 200 (OK)
    assert response.status_code == 200
    # Convert the JSON response into a Python dictionary
    data = response.get_json()
    # Verify that the health status is "healthy"
    assert data["status"] == "healthy"