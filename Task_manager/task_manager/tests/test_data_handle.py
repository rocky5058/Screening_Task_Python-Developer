import unittest
from data_handler import TaskDataHandler
from models import TaskCreate

class TestTaskDataHandler(unittest.TestCase):
    def setUp(self):
        self.handler = TaskDataHandler()

    def test_create_and_get_tasks(self):
        task = TaskCreate(title="Test", description="Unit test")
        created = self.handler.create_task(task)
        tasks = self.handler.get_tasks()
        self.assertTrue(any(t.id == created.id for t in tasks))

    def test_mark_completed(self):
        task = TaskCreate(title="Test", description="Completed test")
        created = self.handler.create_task(task)
        self.handler.mark_completed(created.id)
        updated = [t for t in self.handler.get_tasks() if t.id == created.id][0]
        self.assertTrue(updated.is_completed)

    def test_delete_task(self):
        task = TaskCreate(title="Test", description="Deletion test")
        created = self.handler.create_task(task)
        result = self.handler.delete_task(created.id)
        self.assertTrue(result)
        self.assertFalse(any(t.id == created.id for t in self.handler.get_tasks()))

if __name__ == "__main__":
    unittest.main()
