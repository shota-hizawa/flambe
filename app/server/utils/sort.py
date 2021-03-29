from typing import List
from entities.task import Task, Priority


def sort_tasks_by_priority(tasks: List[Task]) -> List[Task]:
    high_priority_task = list(
        filter(lambda task: task.priority is Priority.HIGH, tasks)
    )
    medium_priority_task = list(
        filter(lambda task: task.priority is Priority.MEDIUM, tasks)
    )
    low_priority_task = list(filter(lambda task: task.priority is Priority.LOW, tasks))

    sorted_tasks = [*high_priority_task, *medium_priority_task, *low_priority_task]

    return sorted_tasks
