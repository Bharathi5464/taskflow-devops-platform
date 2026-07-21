# Import Flask framework
from flask import Flask
# Import function that registers all API routes
from routes import register_routes
# Create Flask application instance
app = Flask(__name__)
# Basic home route# URL: GET http://localhost:5000/
@app.route("/")
def home():
    # Return application information as JSON response
    return {
        "application": "TaskFlow",
        "status": "running",
        "phase": "Phase 1"
    }
# Health check endpoint URL: GET http://localhost:5000/health
@app.route("/health")
def health():
    # Used by monitoring tools/load balancers to check whether application is alive
    return {
        "status": "healthy"
    }
# Register all task-related API routes  This loads routes from routes.py
# Example:
# /tasks
# /tasks/<task_id>

# These routes are separated from app.py
register_routes(app)
# Start Flask development server
# This block runs only when executing:
# python app.py
if __name__ == "__main__":
    # host="0.0.0.0"  Allows access from outside the container/machine
    # port=5000      Flask application listens on port 5000
    # debug=True     Enables auto reload and detailed errors during development
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )