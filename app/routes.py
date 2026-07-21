# Import request to read data sent by the client
# Import jsonify to convert Python dictionaries/lists into JSON responses
from flask import request, jsonify

# Import storage module where CRUD operations are implemented
import storage

# Function to register all API routes with the Flask application
def register_routes(app):
    # GET API endpoint to retrieve all tasks
    # Example: GET http://localhost:5000/tasks
    @app.route("/tasks", methods=["GET"])
    def get_tasks():
        # Fetch all tasks from storage
        # Return the task list as JSON response
        return jsonify(storage.get_all_tasks())

    # GET API endpoint to retrieve a single task by ID
    # Example: GET http://localhost:5000/tasks/1
    @app.route("/tasks/<int:task_id>", methods=["GET"])
    def get_task(task_id):
        # Search for the task using the provided task ID
        task = storage.get_task(task_id)
        # If task exists, return the task details
        if task:
            return jsonify(task)
        # If task does not exist, return error response
        # 404 means "Resource Not Found"
        return jsonify({"error": "Task not found"}), 404

    # POST API endpoint to create a new task
    # Example: POST http://localhost:5000/tasks
    @app.route("/tasks", methods=["POST"])
    def create_task():
        # Read JSON data sent from the client request body
        # Example:
        # {
        #    "title": "Learn Docker"
        # }
        task_data = request.json
        # Create a new task object
        task = {
            # Generate a new ID based on current task count
            "id": len(storage.get_all_tasks()) + 1,
            # Get task title from request data
            "title": task_data["title"],
            # New tasks are incomplete by default
            "completed": False
        }
        # Save the task into storage
        storage.create_task(task)
        # Return created task
        # 201 means "Created successfully"
        return jsonify(task), 201

    # PUT API endpoint to update an existing task
    # Example: PUT http://localhost:5000/tasks/1
    @app.route("/tasks/<int:task_id>", methods=["PUT"])
    def update_task(task_id):
        # Read updated values from request body
        updated_data = request.json
        # Update the task in storage
        task = storage.update_task(
            task_id,
            updated_data
        )
        # If update is successful, return updated task
        if task:
            return jsonify(task)
        # If task does not exist, return 404 error
        return jsonify({"error": "Task not found"}), 404

    # DELETE API endpoint to remove a task
    # Example: DELETE http://localhost:5000/tasks/1
    @app.route("/tasks/<int:task_id>", methods=["DELETE"])
    def delete_task(task_id):
        # Delete task from storage
        # Returns True if deletion is successful
        deleted = storage.delete_task(task_id)
        # If deletion succeeded, return success message
        if deleted:
            return jsonify(
                {"message": "Task deleted"}
            )
        # If task does not exist, return 404 error
        return jsonify({"error": "Task not found"}), 404