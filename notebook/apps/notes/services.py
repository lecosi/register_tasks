from abc import ABC, abstractmethod


class NoteMethod(ABC):

    @abstractmethod
    def create_task(
        self,
        subject: str,
        description: str,
        priority: int,
        user_id: int
    ):
        """creates a task on an initial state and make
        initial validations"""

    @abstractmethod
    def update_task(
        self,
        subject: str,
        description: str,
        priority: int,
        status: int,
        task_id: int
    ):
        """update a task and make validations"""

    @abstractmethod
    def delete_task(
        self,
        task_id: int,
        user_id: int
    ):
        """delete a task and make validations"""


class TaskService(NoteMethod):
    def create_task(
        self,
        subject: str,
        description: str,
        priority: int,
        user_id: int
    ):
        pass

    def update_task(
        self,
        subject: str,
        description: str,
        priority: int,
        status: int,
        task_id: int
    ):
        pass

    def delete_task(
        self,
        task_id: int,
        user_id: int
    ):
        pass

    def get_task_lst_by_user_id(
        self,
        user_id: int
    ):
        pass
