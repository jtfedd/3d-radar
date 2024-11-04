import os
from typing import List

from direct.showbase.ShowBase import ShowBase
from direct.stdpy import threading
from direct.task.Task import Task

from .task import AbstractTask
from .task_status import TaskStatus


class TaskManager:
    def __init__(self, base: ShowBase) -> None:
        self.maxThreads = max(os.cpu_count() or 1, 1)
        self.activeThreads = 0
        self.activeThreadsLock = threading.Lock()

        # Tasks in the queue should be either pending or ready
        self.tasks: List[AbstractTask] = []
        self.tasksLock = threading.Lock()

        print("max threads", self.maxThreads)

        self.updateTask = base.taskMgr.add(self.update, "task-update")

    def addTask(self, task: AbstractTask) -> None:
        print("add task", task.name())
        with self.tasksLock:
            self.tasks.append(task)

    def update(self, task: Task) -> int:
        tasksToProcess: List[AbstractTask] = []
        tasksToPostProcess: List[AbstractTask] = []

        with self.tasksLock:
            filteredTasks = []

            for t in self.tasks:
                # Ignore complete or errored tasks and remove them from the list
                if t.getStatus() in (TaskStatus.COMPLETE, TaskStatus.ERROR):
                    continue

                filteredTasks.append(t)

                if t.getStatus() == TaskStatus.PROCESSING_READY:
                    with self.activeThreadsLock:
                        if self.activeThreads < self.maxThreads:
                            t.processing()
                            tasksToProcess.append(t)

                if t.getStatus() == TaskStatus.POSTPROCESSING_READY:
                    tasksToPostProcess.append(t)

            self.tasks = filteredTasks

        for t in tasksToProcess:
            self.processTask(t)

        for t in tasksToPostProcess:
            t.postProcess()

        return task.cont

    def processTask(self, t: AbstractTask) -> None:
        print("process task", t.name())

        thread = threading.Thread(target=self.runTask, daemon=True, args=(t,))
        thread.start()

    def runTask(self, t: AbstractTask) -> None:
        print("run task", t.name())
        try:
            t.process()
        finally:
            with self.activeThreadsLock:
                self.activeThreads -= 1

    def destroy(self) -> None:
        self.updateTask.cancel()
