def test_home_endpoint(client): # importing the client function from contest.py
    #Verify that the root endpoint ("/") returns HTTP 200 and the expected JSON response.
    # Create a Flask test client This simulates HTTP requests without starting the server
    # Send a GET request to the root endpoint
    response = client.get("/")
    # Verify that the HTTP status code is 200 (Success)
    assert response.status_code == 200
    # Convert the JSON response into a Python dictionary
    data = response.get_json()
    # Verify the returned JSON values
    assert data["application"] == "TaskFlow"
    assert data["status"] == "running"
    assert data["phase"] == "Phase 2"
    assert data["version"] == "v2"