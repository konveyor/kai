import unittest

from kai.reactive_codeplanner.task_manager.api import ValidationError
from kai.reactive_codeplanner.task_manager.priority_queue import PriorityTaskQueue


class TestPriorityTaskQueue(unittest.TestCase):
    def setUp(self):
        self.pq = PriorityTaskQueue()

    def test_priority_basic_order(self):
        pq = PriorityTaskQueue()

        task1 = ValidationError(
            file="test.py", line=1, column=1, message="Task1", priority=0, children=[]
        )
        pq.push(task1)

        task1_child1 = ValidationError(
            file="test.py",
            line=2,
            column=2,
            message="Error1OfDepth1",
            depth=1,
            parent=task1,
            children=[],
        )
        task1.children.append(task1_child1)
        pq.push(task1_child1)

        task1_child2 = ValidationError(
            file="test.py",
            line=3,
            column=3,
            message="Error1OfDepth2",
            depth=2,
            parent=task1_child1,
        )
        task1_child1.children.append(task1_child2)
        pq.push(task1_child2)

        task2 = ValidationError(
            file="test.py", line=4, column=4, message="Task2", priority=0, children=[]
        )
        pq.push(task2)

        task2_child1 = ValidationError(
            file="test.py",
            line=5,
            column=5,
            message="Error2OfDepth1",
            depth=1,
            parent=task2,
            children=[],
        )
        task2.children.append(task2_child1)
        pq.push(task2_child1)

        task2_child2 = ValidationError(
            file="test.py",
            line=6,
            column=6,
            message="Error2OfDepth2",
            depth=2,
            parent=task2_child1,
        )
        task2_child1.children.append(task2_child2)
        pq.push(task2_child2)

        executed_tasks = []
        while pq.all_tasks():
            print(pq)
            executed_tasks.append(pq.pop())

        # Should process by depth first
        expected_order = [
            task1_child2,
            task2_child2,
            task1_child1,
            task2_child1,
            task1,
            task2,
        ]
        self.assertEqual(expected_order, executed_tasks)

    def test_pop_without_max_depth(self):
        task1 = ValidationError(
            file="file1.py", line=10, column=1, message="Task1", priority=1, depth=0
        )
        task2 = ValidationError(
            file="file2.py", line=20, column=2, message="Task2", priority=2, depth=1
        )
        task3 = ValidationError(
            file="file3.py", line=30, column=3, message="Task3", priority=1, depth=2
        )

        self.pq.push(task1)
        self.pq.push(task2)
        self.pq.push(task3)

        popped_tasks = []
        while self.pq.all_tasks():
            popped_tasks.append(self.pq.pop())

        # Assert that tasks are popped in the correct priority order
        expected_order = [task3, task1, task2]
        self.assertEqual(popped_tasks, expected_order)

    def test_pop_with_max_depth(self):
        task1 = ValidationError(
            file="file1.py", line=10, column=1, message="Task1", priority=1, depth=0
        )
        task2 = ValidationError(
            file="file2.py", line=20, column=2, message="Task2", priority=1, depth=1
        )
        task3 = ValidationError(
            file="file3.py", line=30, column=3, message="Task3", priority=1, depth=2
        )

        self.pq.push(task1)
        self.pq.push(task2)
        self.pq.push(task3)

        popped_tasks = []
        while True:
            try:
                task = self.pq.pop(max_depth=1)
                popped_tasks.append(task)
            except IndexError:
                break  # No more tasks within max_depth

        # Assert that only tasks with depth <= 1 are popped
        expected_tasks = [task2, task1]
        self.assertEqual(popped_tasks, expected_tasks)

        # Ensure tasks with depth > 1 are still in the queue
        remaining_tasks = self.pq.all_tasks()
        self.assertIn(task3, remaining_tasks)
        self.assertEqual(len(remaining_tasks), 1)

    def test_pop_with_no_tasks_within_max_depth(self):
        task1 = ValidationError(
            file="file1.py", line=10, column=1, message="Task1", priority=1, depth=2
        )
        task2 = ValidationError(
            file="file2.py", line=20, column=2, message="Task2", priority=1, depth=3
        )

        self.pq.push(task1)
        self.pq.push(task2)

        with self.assertRaises(IndexError) as context:
            self.pq.pop(max_depth=1)

        # Assert that the correct exception is raised
        self.assertEqual(
            str(context.exception),
            "No tasks available within the specified max_depth of 1",
        )

        # Ensure all tasks are still in the queue
        remaining_tasks = self.pq.all_tasks()
        self.assertEqual(len(remaining_tasks), 2)

    def test_pop_with_mixed_depths_and_priorities(self):
        task_low_priority_low_depth = ValidationError(
            file="file1.py",
            line=10,
            column=1,
            message="LowPriorityLowDepth",
            priority=2,
            depth=0,
        )
        task_high_priority_high_depth = ValidationError(
            file="file2.py",
            line=20,
            column=2,
            message="HighPriorityHighDepth",
            priority=1,
            depth=2,
        )
        task_high_priority_low_depth = ValidationError(
            file="file3.py",
            line=30,
            column=3,
            message="HighPriorityLowDepth",
            priority=1,
            depth=1,
        )

        self.pq.push(task_low_priority_low_depth)
        self.pq.push(task_high_priority_high_depth)
        self.pq.push(task_high_priority_low_depth)

        popped_tasks = []
        while True:
            try:
                task = self.pq.pop(max_depth=1)
                popped_tasks.append(task)
            except IndexError:
                break  # No more tasks within max_depth

        # Assert that tasks are popped in correct order considering priority and depth
        expected_tasks = [task_high_priority_low_depth, task_low_priority_low_depth]
        self.assertEqual(popped_tasks, expected_tasks)

        # Ensure the high-depth task is still in the queue
        remaining_tasks = self.pq.all_tasks()
        self.assertIn(task_high_priority_high_depth, remaining_tasks)
        self.assertEqual(len(remaining_tasks), 1)

    def test_pop_all_tasks_with_max_depth_none(self):
        tasks = [
            ValidationError(
                file=f"file{i}.py",
                line=i,
                column=1,
                message=f"Task{i}",
                priority=i % 3,
                depth=i % 2,
            )
            for i in range(5)
        ]

        for task in tasks:
            self.pq.push(task)

        popped_tasks = []
        while True:
            try:
                task = self.pq.pop()
                popped_tasks.append(task)
            except IndexError:
                break  # No more tasks

        # Assert that all tasks have been popped
        self.assertEqual(len(popped_tasks), len(tasks))
        self.assertEqual(self.pq.all_tasks(), set())

    def test_pop_with_changing_max_depth(self):
        task_depth_0 = ValidationError(
            file="file1.py", line=10, column=1, message="Depth0", priority=1, depth=0
        )
        task_depth_1 = ValidationError(
            file="file2.py", line=20, column=2, message="Depth1", priority=1, depth=1
        )
        task_depth_2 = ValidationError(
            file="file3.py", line=30, column=3, message="Depth2", priority=1, depth=2
        )

        self.pq.push(task_depth_0)
        self.pq.push(task_depth_1)
        self.pq.push(task_depth_2)

        popped_tasks = []
        while True:
            try:
                task = self.pq.pop(max_depth=0)
                popped_tasks.append(task)
            except IndexError:
                break

        # Assert that only depth 0 tasks are popped
        self.assertEqual(popped_tasks, [task_depth_0])

        # Pop tasks with max_depth=1
        while True:
            try:
                task = self.pq.pop(max_depth=1)
                popped_tasks.append(task)
            except IndexError:
                break

        # Assert that depth 1 tasks are popped
        self.assertEqual(popped_tasks, [task_depth_0, task_depth_1])

        # Pop remaining tasks without max_depth
        while True:
            try:
                task = self.pq.pop()
                popped_tasks.append(task)
            except IndexError:
                break

        # Assert that all tasks are now popped
        self.assertEqual(popped_tasks, [task_depth_0, task_depth_1, task_depth_2])
        self.assertEqual(self.pq.all_tasks(), set())

    def test_pop_maintains_task_stack_integrity(self):
        task1 = ValidationError(
            file="file1.py", line=10, column=1, message="Task1", priority=1, depth=1
        )
        task2 = ValidationError(
            file="file2.py", line=20, column=2, message="Task2", priority=1, depth=2
        )
        task3 = ValidationError(
            file="file3.py", line=30, column=3, message="Task3", priority=1, depth=3
        )

        self.pq.push(task1)
        self.pq.push(task2)
        self.pq.push(task3)

        popped_tasks = []
        while True:
            try:
                task = self.pq.pop(max_depth=2)
                popped_tasks.append(task)
            except IndexError:
                break

        # Assert that tasks with depth <= 2 are popped
        expected_tasks = [task2, task1]  # Popped in stack order
        self.assertEqual(popped_tasks, expected_tasks)

        # Ensure task with depth > 2 remains in the queue
        remaining_tasks = list(self.pq.all_tasks())
        self.assertEqual(remaining_tasks, [task3])

    def test_pop_removes_empty_priority_levels(self):
        task_priority_1 = ValidationError(
            file="file1.py", line=10, column=1, message="Priority1", priority=1, depth=0
        )
        task_priority_2 = ValidationError(
            file="file2.py", line=20, column=2, message="Priority2", priority=2, depth=0
        )

        self.pq.push(task_priority_1)
        self.pq.push(task_priority_2)

        while True:
            try:
                self.pq.pop()
            except IndexError:
                break

        # Assert that task_stacks is empty
        self.assertEqual(self.pq.task_stacks, {})

    def test_pop_with_none_max_depth_returns_highest_priority_task(self):
        task1 = ValidationError(
            file="file1.py", line=10, column=1, message="Task1", priority=2, depth=1
        )
        task2 = ValidationError(
            file="file2.py", line=20, column=2, message="Task2", priority=1, depth=2
        )

        self.pq.push(task1)
        self.pq.push(task2)

        task = self.pq.pop()

        # Assert that the highest priority task is returned regardless of depth
        self.assertEqual(task, task2)

    def test_pop_with_no_tasks_raises_exception(self):
        # Attempt to pop from an empty queue
        with self.assertRaises(IndexError) as context:
            self.pq.pop()

        # Assert that the correct exception is raised
        self.assertEqual(str(context.exception), "Pop from empty PriorityTaskQueue")

    def test_has_tasks_within_depth(self):
        task_depth_1 = ValidationError(
            file="file1.py", line=10, column=1, message="Depth1", priority=1, depth=1
        )
        task_depth_3 = ValidationError(
            file="file2.py", line=20, column=2, message="Depth3", priority=1, depth=3
        )

        self.pq.push(task_depth_1)
        self.pq.push(task_depth_3)

        # Check for tasks within depth
        self.assertTrue(self.pq.has_tasks_within_depth(1))
        self.assertTrue(self.pq.has_tasks_within_depth(3))
        self.assertFalse(self.pq.has_tasks_within_depth(0))


if __name__ == "__main__":
    unittest.main()
