import unittest
from typing import List

# Import classes from your codebase
from playpen.repo_level_awareness.api import (
    RpcClientConfig,
    Task,
    TaskResult,
    ValidationError,
    ValidationResult,
    ValidationStep,
)
from playpen.repo_level_awareness.codeplan import TaskManager


class MockValidationStep(ValidationStep):
    def __init__(
        self, config: RpcClientConfig, error_sequences: List[List[ValidationError]]
    ):
        super().__init__(config)
        self.error_sequences = error_sequences
        self.run_count = 0

    def run(self) -> ValidationResult:
        if self.run_count < len(self.error_sequences):
            errors = self.error_sequences[self.run_count]
        else:
            errors = []
        self.run_count += 1
        passed = len(errors) == 0
        return ValidationResult(passed=passed, errors=errors)


class MockTaskRunner:
    def can_handle_task(self, task: Task) -> bool:
        return True  # For testing, assume it can handle any task

    def execute_task(self, rcm, task: Task) -> TaskResult:
        # Simulate task execution by returning a TaskResult
        return TaskResult(encountered_errors=[], modified_files=[])


class TestTaskManager(unittest.TestCase):
    def test_simple_task_execution_order(self):
        # Setup
        validator = MockValidationStep(
            config=None,
            error_sequences=[
                [
                    ValidationError(file="test.py", line=1, column=1, message="Error1")
                ],  # First run
                [],  # Second run, no errors
            ],
        )
        task_manager = TaskManager(
            config=None,
            rcm=None,
            updated_file_content=None,
            validators=[validator],
            agents=[MockTaskRunner()],
        )

        # Collect executed tasks
        executed_tasks = []

        # Execute tasks
        for task in task_manager.get_next_task():
            executed_tasks.append(task)

        # Assertions
        self.assertEqual(len(executed_tasks), 1)
        self.assertEqual(executed_tasks[0].message, "Error1")

    def test_task_with_children_dfs_order(self):
        # Setup
        validator = MockValidationStep(
            config=None,
            error_sequences=[
                [
                    ValidationError(
                        file="test.py", line=1, column=1, message="ParentError"
                    )
                ],  # First run
                [
                    ValidationError(
                        file="test.py",
                        line=2,
                        column=1,
                        message="ChildError1",
                        priority=4,
                    ),
                    ValidationError(
                        file="test.py", line=3, column=1, message="ChildError2"
                    ),
                ],  # Second run
                [],  # Third run, no errors
            ],
        )
        task_manager = TaskManager(
            config=None,
            rcm=None,
            updated_file_content=None,
            validators=[validator],
            agents=[MockTaskRunner()],
        )

        executed_tasks = []

        for task in task_manager.get_next_task():
            executed_tasks.append(task)

        self.assertEqual(len(executed_tasks), 3)
        self.assertEqual(
            [t.message for t in executed_tasks],
            ["ParentError", "ChildError1", "ChildError2"],
        )
        self.assertTrue(executed_tasks[1].depth > executed_tasks[0].depth)
        self.assertTrue(executed_tasks[2].depth > executed_tasks[0].depth)

    def test_task_retry_logic(self):
        # Setup
        validator = MockValidationStep(
            config=None,
            error_sequences=[
                [
                    ValidationError(
                        file="test.py", line=1, column=1, message="PersistentError"
                    )
                ],  # First run
                [
                    ValidationError(
                        file="test.py", line=1, column=1, message="PersistentError"
                    )
                ],  # Second run
                [
                    ValidationError(
                        file="test.py", line=1, column=1, message="PersistentError"
                    )
                ],  # Third run
                [
                    ValidationError(
                        file="test.py", line=1, column=1, message="PersistentError"
                    )
                ],  # Fourth run
                [],  # Fifth run, error resolved
            ],
        )
        task_manager = TaskManager(
            config=None,
            rcm=None,
            updated_file_content=None,
            validators=[validator],
            agents=[MockTaskRunner()],
        )

        executed_tasks = []
        retries = 0

        for task in task_manager.get_next_task():
            executed_tasks.append(task)
            if task.retry_count > 0:
                retries += 1

        self.assertEqual(len(executed_tasks), 3)  # max_retries is 3
        self.assertEqual(executed_tasks[0].message, "PersistentError")
        self.assertEqual(executed_tasks[0].retry_count, 0)
        self.assertEqual(executed_tasks[1].retry_count, 1)
        self.assertEqual(executed_tasks[2].retry_count, 2)
        self.assertEqual(retries, 2)  # Retries occurred twice

    def test_handling_ignored_tasks(self):
        # Setup
        validator = MockValidationStep(
            config=None,
            error_sequences=[
                [
                    ValidationError(
                        file="test.py", line=1, column=1, message="UnresolvableError"
                    )
                ],  # First run
                [
                    ValidationError(
                        file="test.py", line=1, column=1, message="UnresolvableError"
                    )
                ],  # Second run
                [
                    ValidationError(
                        file="test.py", line=1, column=1, message="UnresolvableError"
                    )
                ],  # Third run
                [
                    ValidationError(
                        file="test.py", line=1, column=1, message="UnresolvableError"
                    )
                ],  # Fourth run
                [
                    ValidationError(
                        file="test.py", line=1, column=1, message="UnresolvableError"
                    )
                ],  # Fifth run
            ],
        )
        task_manager = TaskManager(
            config=None,
            rcm=None,
            updated_file_content=None,
            validators=[validator],
            agents=[MockTaskRunner()],
        )

        for _task in task_manager.get_next_task():
            pass

        self.assertEqual(len(task_manager.ignored_tasks), 1)
        ignored_task = task_manager.ignored_tasks[0]
        self.assertEqual(ignored_task.message, "UnresolvableError")
        self.assertEqual(ignored_task.retry_count, ignored_task.max_retries)

    def test_complex_task_tree(self):
        # Setup
        validator = MockValidationStep(
            config=None,
            error_sequences=[
                [
                    ValidationError(
                        file="test.py", line=1, column=1, message="ParentError"
                    )
                ],  # First run
                [
                    ValidationError(
                        file="test.py",
                        line=2,
                        column=1,
                        message="ChildError1",
                        priority=4,
                    ),
                    ValidationError(
                        file="test.py", line=3, column=1, message="ChildError2"
                    ),
                ],  # Second run
                [],  # Third run, no new errors
                [
                    ValidationError(
                        file="test.py", line=4, column=1, message="GrandchildError"
                    )
                ],  # Fourth run
                [],  # Fifth run, no errors
            ],
        )
        task_manager = TaskManager(
            config=None,
            rcm=None,
            updated_file_content=None,
            validators=[validator],
            agents=[MockTaskRunner()],
        )

        executed_tasks = []

        for task in task_manager.get_next_task():
            executed_tasks.append(task)

        self.assertEqual(len(executed_tasks), 4)
        parent, child1, child2, grandchild = executed_tasks

        self.assertEqual(parent.message, "ParentError")
        self.assertEqual(parent.depth, 0)
        self.assertEqual(len(parent.children), 2)

        self.assertEqual(child1.message, "ChildError1")
        self.assertEqual(child1.depth, 1)
        self.assertEqual(len(child1.children), 0)
        self.assertEqual(parent, child1.parent)

        self.assertEqual(child2.message, "ChildError2")
        self.assertEqual(child2.depth, 1)
        self.assertEqual(len(child2.children), 1)
        self.assertEqual(parent, child2.parent)

        self.assertEqual(grandchild.message, "GrandchildError")
        self.assertEqual(grandchild.depth, 2)
        self.assertEqual(len(grandchild.children), 0)
        self.assertEqual(child2, grandchild.parent)


if __name__ == "__main__":
    unittest.main()
