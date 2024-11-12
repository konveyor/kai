import unittest

# Import classes from your codebase
from kai.reactive_codeplanner.task_manager.api import (
    RpcClientConfig,
    Task,
    TaskResult,
    ValidationError,
    ValidationResult,
    ValidationStep,
)
from kai.reactive_codeplanner.task_manager.priority_queue import PriorityTaskQueue
from kai.reactive_codeplanner.task_manager.task_manager import TaskManager


class MockValidationStep(ValidationStep):
    def __init__(
        self, config: RpcClientConfig, error_sequences: list[list[ValidationError]]
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
            validators=[validator],
            task_runners=[MockTaskRunner()],
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
        parent = ValidationError(
            file="test.py", line=1, column=1, message="ParentError"
        )
        child1 = ValidationError(
            file="test.py", line=2, column=1, message="ChildError1"
        )
        child2 = ValidationError(
            file="test.py", line=3, column=1, message="ChildError2"
        )

        validator = MockValidationStep(
            config=None,
            error_sequences=[
                [parent],  # First run
                [child1, child2],  # Second run
                [child2],  # Third run, no new errors
            ],
        )
        task_manager = TaskManager(
            config=None,
            rcm=None,
            validators=[validator],
            task_runners=[MockTaskRunner()],
        )

        executed_tasks = []

        for task in task_manager.get_next_task():
            executed_tasks.append(task)

        self.assertEqual(len(executed_tasks), 3)
        parent, child1, child2 = executed_tasks

        self.assertEqual(parent.message, "ParentError")
        self.assertEqual(child2.message, "ChildError2")
        self.assertEqual(child1.message, "ChildError1")
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
            validators=[validator],
            task_runners=[MockTaskRunner()],
        )

        executed_tasks = []
        retries = 0

        for task in task_manager.get_next_task():
            executed_tasks.append(task)
            if task.retry_count > 0:
                retries += 1

        self.assertEqual(len(executed_tasks), 3)  # max_retries is 3
        self.assertEqual(executed_tasks[0].message, "PersistentError")
        self.assertEqual(executed_tasks[2].retry_count, 3)
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
            validators=[validator],
            task_runners=[MockTaskRunner()],
        )

        for _task in task_manager.get_next_task():
            pass

        self.assertEqual(len(task_manager.ignored_tasks), 1)
        ignored_task = task_manager.ignored_tasks[0]
        self.assertEqual(ignored_task.message, "UnresolvableError")
        self.assertEqual(ignored_task.retry_count, ignored_task.max_retries)

    def test_complex_task_tree(self):

        parent = ValidationError(
            file="test.py", line=1, column=1, message="ParentError", priority=3
        )
        toplevel = ValidationError(
            file="test.py", line=1, column=1, message="TopLevelError", priority=4
        )
        child1 = ValidationError(
            file="test.py", line=2, column=1, message="ChildError1"
        )
        child2 = ValidationError(
            file="test.py", line=4, column=1, message="ChildError2"
        )
        grandchild = ValidationError(
            file="test.py", line=4, column=1, message="GrandchildError"
        )

        # Setup
        validator = MockValidationStep(
            config=None,
            error_sequences=[
                [parent, toplevel],  # First run
                [child1, child2, toplevel],  # Second run
                [child2, toplevel],  # Third run, no new errors
                [grandchild, toplevel],  # Fourth run
                [toplevel],  # Fifth run, no new errors
                [],  # Sixth run, no errors
            ],
        )
        task_manager = TaskManager(
            config=None,
            rcm=None,
            validators=[validator],
            task_runners=[MockTaskRunner()],
        )

        executed_tasks = []

        for task in task_manager.get_next_task():
            executed_tasks.append(task)

        self.assertEqual(len(executed_tasks), 5)
        parent, child1, child2, grandchild, toplevel = executed_tasks

        self.assertEqual(parent.message, "ParentError")
        self.assertEqual(parent.depth, 0)
        self.assertEqual(len(parent.children), 2)

        self.assertEqual(child1.message, "ChildError1")
        self.assertEqual(child1.depth, 1)
        self.assertEqual(len(child1.children), 0)
        self.assertEqual(parent, child1.parent)

        self.assertEqual(child2.message, "ChildError2")
        self.assertEqual(child2.depth, 1)
        self.assertEqual(child2.children[0], grandchild)
        self.assertEqual(len(child2.children), 1)
        self.assertEqual(parent, child2.parent)

        self.assertEqual(grandchild.message, "GrandchildError")
        self.assertEqual(grandchild.depth, 2)
        self.assertEqual(len(grandchild.children), 0)
        self.assertEqual(child2, grandchild.parent)

        self.assertEqual(toplevel.message, "TopLevelError")
        self.assertEqual(toplevel.depth, 0)
        self.assertEqual(len(toplevel.children), 0)

    def test_stop_iteration_with_seed(self):
        # Setup
        parent = ValidationError(
            file="test.py", line=1, column=1, message="ParentError", priority=3
        )
        toplevel = ValidationError(
            file="test.py", line=1, column=1, message="TopLevelError", priority=4
        )
        child1 = ValidationError(
            file="test.py", line=2, column=1, message="ChildError1"
        )
        child2 = ValidationError(
            file="test.py", line=4, column=1, message="ChildError2"
        )
        grandchild = ValidationError(
            file="test.py", line=4, column=1, message="GrandchildError"
        )

        validator = MockValidationStep(
            config=None,
            error_sequences=[
                [parent, toplevel],  # First run
                [child1, child2, toplevel],  # Second run
                [child1, toplevel],  # Third run, no new errors
                [grandchild, toplevel],  # Fourth run
                [toplevel],  # Fifth run, no new errors
            ],
        )
        seed_tasks = [
            ValidationError(
                file="test.py",
                line=1,
                column=1,
                message="ParentError",
            )
        ]
        task_manager = TaskManager(
            config=None,
            rcm=None,
            seed_tasks=seed_tasks,
            validators=[validator],
            task_runners=[MockTaskRunner()],
        )

        executed_tasks = []

        # Priority 0 means only seed issues and associated children will be processed
        for task in task_manager.get_next_task(max_priority=0):
            executed_tasks.append(task)

        self.assertEqual(len(executed_tasks), 4)
        self.assertIn(
            toplevel, task_manager.priority_queue.task_stacks[toplevel.priority]
        )
        self.assertNotIn(toplevel, executed_tasks)

        for task in task_manager.get_next_task(max_priority=10):
            executed_tasks.append(task)

        self.assertEqual(len(executed_tasks), 5)
        self.assertEqual(toplevel, executed_tasks[-1])
        self.assertEqual(task_manager.priority_queue.task_stacks, {})

    def test_max_depth_handling(self):
        # Setup
        # Validator returns a parent error, which reveals child errors, and so on
        errorlevel0 = ValidationError(
            file="test.py", line=0, column=0, message="ErrorLevel0"
        )
        errorlevel1 = ValidationError(
            file="test.py", line=1, column=1, message="ErrorLevel1"
        )
        errorlevel2 = ValidationError(
            file="test.py", line=2, column=2, message="ErrorLevel2"
        )
        errorlevel3 = ValidationError(
            file="test.py", line=3, column=3, message="ErrorLevel3"
        )
        validator = MockValidationStep(
            config=None,
            error_sequences=[
                [errorlevel0],  # First run
                [errorlevel1],  # Second run
                [errorlevel2],  # Third run
                [errorlevel2],  # fourth run (same since we start the task queue again)
                [errorlevel3],  # Fifth run
                [],  # Fifth run, no errors
            ],
        )
        task_manager = TaskManager(
            config=None,
            rcm=None,
            validators=[validator],
            task_runners=[MockTaskRunner()],
        )

        executed_tasks = []

        # Set max_depth to 1 (top-level children only)
        max_depth = 1

        for task in task_manager.get_next_task(max_depth=max_depth):
            executed_tasks.append((task.depth, task.message))

        # Expected tasks: only those with depth <= max_depth
        expected_tasks = [
            (0, "ErrorLevel0"),  # Depth 0
            (1, "ErrorLevel1"),  # Depth 1
        ]

        self.assertEqual(executed_tasks, expected_tasks)

        # Ensure that tasks beyond max_depth are marked as processed
        task_depths = [depth for depth, _ in executed_tasks]
        self.assertTrue(all(depth <= max_depth for depth in task_depths))

        # Verify that tasks at depth greater than max_depth are not executed
        self.assertNotIn((2, "ErrorLevel2"), executed_tasks)
        self.assertNotIn((3, "ErrorLevel3"), executed_tasks)

        max_depth = 10
        for task in task_manager.get_next_task(max_depth=max_depth):
            executed_tasks.append((task.depth, task.message))

        self.assertIn((2, "ErrorLevel2"), executed_tasks)
        self.assertIn((3, "ErrorLevel3"), executed_tasks)


if __name__ == "__main__":
    unittest.main()
