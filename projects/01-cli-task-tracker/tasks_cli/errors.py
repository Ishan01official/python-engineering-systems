"""Custom exceptions for the task tracker."""


class TaskError(Exception):
    """Base for tasks-cli errors."""


class TaskNotFound(TaskError):
    def __init__(self, task_id: int):
        super().__init__(f"task {task_id} not found")
        self.task_id = task_id
