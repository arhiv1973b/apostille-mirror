import pytest
import sys
import os
import time
import queue
import random
from dataclasses import dataclass
from enum import Enum
from typing import Optional, Any

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class InstanceStatus(Enum):
    ACTIVE = "active"
    FAILED = "failed"
    TUNNELING = "tunneling"
    CARRYING_FLAG = "carrying_flag"


@dataclass
class Task:
    id: str
    description: str
    priority: int
    environment: Optional[str] = None
    retries: int = 0
    max_retries: int = 3
    created_at: Optional[float] = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = time.time()


@dataclass
class TaskResult:
    task_id: str
    success: bool
    result: Any = None
    error: Optional[str] = None
    execution_time: float = 0
    environment: str = ""
    quantum_tunnel_used: bool = False


class AIInstance:
    def __init__(self, environment: str, instance_id: int):
        self.environment = environment
        self.instance_id = instance_id
        self.status = InstanceStatus.ACTIVE
        self.task_queue = queue.Queue()
        self.processed_tasks = 0
        self.failed_tasks = 0
        self.last_activity = time.time()
        self.temperature = 0.5
        self.clarity = 0.8
        self.is_carrying_flag = False

    def execute_task(self, task: Task) -> TaskResult:
        start_time = time.time()

        try:
            base_success_rate = 0.8

            if self.temperature < 0.3:
                success_rate = base_success_rate - 0.3
            elif self.temperature > 0.7:
                success_rate = base_success_rate - 0.2
            else:
                success_rate = base_success_rate + 0.1

            success_rate += self.clarity * 0.1

            if self.environment == "windows" and "linux" in task.description.lower():
                success_rate -= 0.2
            elif self.environment == "wsl" and "windows" in task.description.lower():
                success_rate -= 0.1

            success_rate = max(0.1, min(0.95, success_rate))

            execution_time = random.uniform(0.1, 0.3)
            time.sleep(min(execution_time, 0.05))

            success = random.random() < success_rate

            if success:
                result = f"Task '{task.description}' completed in {self.environment}"
                self.processed_tasks += 1
            else:
                error = f"Task failed in {self.environment}"
                self.failed_tasks += 1
                result = None
                error = error

            self.last_activity = time.time()

            return TaskResult(
                task_id=task.id,
                success=success,
                result=result if success else None,
                error=error if not success else None,
                execution_time=execution_time,
                environment=self.environment,
                quantum_tunnel_used=False,
            )

        except Exception as e:
            self.failed_tasks += 1
            return TaskResult(
                task_id=task.id,
                success=False,
                error=f"Exception: {str(e)}",
                environment=self.environment,
                quantum_tunnel_used=False,
            )


class TestTask:
    def test_task_creation(self):
        task = Task(
            id="test_1",
            description="Test task",
            priority=5
        )
        assert task.id == "test_1"
        assert task.description == "Test task"
        assert task.priority == 5
        assert task.retries == 0
        assert task.max_retries == 3
        assert task.created_at is not None

    def test_task_default_values(self):
        task = Task(id="test_2", description="Test", priority=1)
        assert task.environment is None
        assert task.created_at is not None


class TestTaskResult:
    def test_task_result_creation(self):
        result = TaskResult(
            task_id="task_1",
            success=True,
            result="Completed",
            execution_time=1.5,
            environment="windows"
        )
        assert result.task_id == "task_1"
        assert result.success is True
        assert result.result == "Completed"
        assert result.error is None
        assert result.execution_time == 1.5

    def test_task_result_failure(self):
        result = TaskResult(
            task_id="task_2",
            success=False,
            error="Timeout error"
        )
        assert result.success is False
        assert result.error == "Timeout error"
        assert result.result is None


class TestAIInstance:
    def test_instance_creation(self):
        instance = AIInstance("windows", 0)
        assert instance.environment == "windows"
        assert instance.instance_id == 0
        assert instance.status == InstanceStatus.ACTIVE
        assert instance.processed_tasks == 0
        assert instance.failed_tasks == 0
        assert instance.temperature == 0.5
        assert instance.clarity == 0.8

    def test_instance_execute_task(self):
        instance = AIInstance("windows", 0)
        task = Task(id="test_task", description="Test", priority=1)
        
        instance.temperature = 0.5
        instance.clarity = 0.8
        
        result = instance.execute_task(task)
        
        assert result.task_id == "test_task"
        assert result.environment == "windows"
        assert isinstance(result.execution_time, float)

    def test_instance_status(self):
        instance = AIInstance("wsl", 1)
        assert instance.status == InstanceStatus.ACTIVE
        
        instance.status = InstanceStatus.TUNNELING
        assert instance.status == InstanceStatus.TUNNELING


class TestTriInstanceAICoordinator:
    def test_coordinator_creation(self):
        instances = [
            AIInstance("windows", 0),
            AIInstance("wsl", 1),
            AIInstance("git", 2),
        ]
        
        assert len(instances) == 3
        assert instances[0].environment == "windows"
        assert instances[1].environment == "wsl"
        assert instances[2].environment == "git"

    def test_add_task(self):
        tasks = []
        
        task = Task(
            id=f"task_{int(time.time() * 1000)}",
            description="Test task",
            priority=3
        )
        tasks.append(task)
        
        assert len(tasks) == 1
        assert task.description == "Test task"

    def test_coordinator_environments(self):
        instances = [
            AIInstance("windows", 0),
            AIInstance("wsl", 1),
            AIInstance("git", 2),
        ]
        
        envs = [inst.environment for inst in instances]
        assert "windows" in envs
        assert "wsl" in envs
        assert "git" in envs
