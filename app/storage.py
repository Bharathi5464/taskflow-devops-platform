# In-memory list to store tasks
# Currently, data will be stored only in application memory.
# When the Flask app restarts, all tasks will be lost.
tasks = []
# Function to retrieve all tasks
def get_all_tasks():
    # Return the complete task list
    return tasks


# Function to retrieve a single task using its ID
def get_task(task_id):
    # Loop through each task in the tasks list
    for task in tasks:
        # Check whether the current task ID matches the requested ID
        if task["id"] == task_id:
            # Return the matching task
            return task
    # If no task is found with the given ID, return None
    return None

# Function to create a new task
def create_task(task):
    # Add the new task dictionary into the tasks list
    tasks.append(task)
    # Return the newly created task
    return task

# Function to update an existing task
def update_task(task_id, updated_task):
    # Search for the task that needs to be updated
    for task in tasks:
        # Check if the task ID matches
        if task["id"] == task_id:
            # Update existing task fields with new values
            task.update(updated_task)
            # Return the updated task
            return task
    # If task is not found, return None
    return None

# Function to delete a task
def delete_task(task_id):
    # Search for the task that needs to be deleted
    for task in tasks:
        # Check whether the task ID matches
        if task["id"] == task_id:
            # Remove the task from the list
            tasks.remove(task)
            # Return True to indicate successful deletion
            return True
    # Return False if no task was found
    return False