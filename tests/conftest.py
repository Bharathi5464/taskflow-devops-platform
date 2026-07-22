# Import the sys module Used to modify Python's module search path
import sys
# Import Path for handling file and directory paths
from pathlib import Path
# Import pytest testing framework
import pytest
# Add the "app" directory to Python's module search path This allows the test files to import app.py even though they are inside the tests/ folder
sys.path.append(
    str(Path(__file__).resolve().parent.parent / "app")
)
# Import the Flask application instance
from app import app
# Create a reusable pytest fixture The fixture provides a Flask test client to any test function that requests the "client" parameter
@pytest.fixture
def client():
    #Create a Flask test client  for automated API testing.
    # Return a Flask test client# It simulates HTTP requests without starting a real server
    return app.test_client()