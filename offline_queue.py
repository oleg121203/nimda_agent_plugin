#!/usr/bin/env python3
"""
Offline Queue System for NIMDA Agent
Ensures operations are not lost when network is unavailable
"""

import json
import logging
import threading
import time
import uuid
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Callable, Dict, List, Optional

import requests

# Setup logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class OperationType(Enum):
    """Types of operations that can be queued"""

    GIT_SYNC = "git_sync"
    GIT_PUSH = "git_push"
    GIT_PULL = "git_pull"
    GIT_COMMIT = "git_commit"
    CODEX_SYNC = "codex_sync"
    BACKUP_CREATE = "backup_create"
    DEV_PLAN_UPDATE = "dev_plan_update"
    CHANGELOG_UPDATE = "changelog_update"
    FILE_OPERATION = "file_operation"
    CUSTOM = "custom"


class OperationStatus(Enum):
    """Status of queued operations"""

    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    RETRYING = "retrying"
    CANCELLED = "cancelled"


@dataclass
class QueuedOperation:
    """A single operation in the queue"""

    id: str
    operation_type: OperationType
    timestamp: str
    status: OperationStatus
    priority: int  # Higher number = higher priority
    max_retries: int
    retry_count: int
    retry_delay: int  # seconds
    next_retry: str  # ISO timestamp
    data: dict
    result: Optional[dict] = None
    error: Optional[str] = None

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization"""
        return {
            "id": self.id,
            "operation_type": self.operation_type.value,
            "timestamp": self.timestamp,
            "status": self.status.value,
            "priority": self.priority,
            "max_retries": self.max_retries,
            "retry_count": self.retry_count,
            "retry_delay": self.retry_delay,
            "next_retry": self.next_retry,
            "data": self.data,
            "result": self.result,
            "error": self.error,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "QueuedOperation":
        """Create from dictionary"""
        return cls(
            id=data["id"],
            operation_type=OperationType(data["operation_type"]),
            timestamp=data["timestamp"],
            status=OperationStatus(data["status"]),
            priority=data["priority"],
            max_retries=data["max_retries"],
            retry_count=data["retry_count"],
            retry_delay=data["retry_delay"],
            next_retry=data["next_retry"],
            data=data["data"],
            result=data.get("result"),
            error=data.get("error"),
        )


class NetworkMonitor:
    """Monitor network connectivity"""

    def __init__(self, timeout: int = 5):
        self.timeout = timeout
        self.test_urls = [
            "https://8.8.8.8",  # Google DNS
            "https://1.1.1.1",  # Cloudflare DNS
            "https://github.com",  # GitHub
        ]

    def is_online(self) -> bool:
        """Check if network is available"""
        for url in self.test_urls:
            try:
                response = requests.get(url, timeout=self.timeout)
                if response.status_code == 200:
                    return True
            except (requests.RequestException, Exception):
                continue
        return False

    def wait_for_connection(self, max_wait: int = 300) -> bool:
        """Wait for network connection to become available"""
        start_time = time.time()

        while time.time() - start_time < max_wait:
            if self.is_online():
                return True
            time.sleep(10)  # Check every 10 seconds

        return False


class OfflineQueue:
    """Queue system for offline operations"""

    def __init__(
        self, queue_file: str = ".nimda_offline_queue.json", max_queue_size: int = 1000
    ):
        self.queue_file = Path(queue_file)
        self.max_queue_size = max_queue_size
        self.operations: List[QueuedOperation] = []
        self.network_monitor = NetworkMonitor()
        self.processing = False
        self.processor_thread = None
        self.operation_handlers: Dict[OperationType, Callable] = {}

        # Load existing queue
        self.load_queue()

        # Default retry settings
        self.default_max_retries = 3
        self.default_retry_delay = 60  # 1 minute

    def register_handler(self, operation_type: OperationType, handler: Callable):
        """Register handler for specific operation type"""
        self.operation_handlers[operation_type] = handler
        logger.info(f"Registered handler for {operation_type.value}")

    def load_queue(self):
        """Load queue from file"""
        try:
            if self.queue_file.exists():
                with open(self.queue_file, "r", encoding="utf-8") as f:
                    data = json.load(f)

                self.operations = [
                    QueuedOperation.from_dict(op_data)
                    for op_data in data.get("operations", [])
                ]

                logger.info(f"Loaded {len(self.operations)} operations from queue")
            else:
                self.operations = []
                logger.info("No existing queue file found, starting fresh")

        except Exception as e:
            logger.error(f"Error loading queue: {e}")
            self.operations = []

    def save_queue(self):
        """Save queue to file"""
        try:
            queue_data = {
                "last_updated": datetime.now().isoformat(),
                "operations": [op.to_dict() for op in self.operations],
            }

            with open(self.queue_file, "w", encoding="utf-8") as f:
                json.dump(queue_data, f, indent=2, ensure_ascii=False)

            logger.debug("Queue saved to file")

        except Exception as e:
            logger.error(f"Error saving queue: {e}")

    def enqueue_operation(
        self,
        operation_type: OperationType,
        data: dict,
        priority: int = 5,
        max_retries: Optional[int] = None,
        retry_delay: Optional[int] = None,
    ) -> str:
        """Add operation to queue"""

        if len(self.operations) >= self.max_queue_size:
            # Remove oldest completed operations
            self._cleanup_completed_operations()

            if len(self.operations) >= self.max_queue_size:
                raise Exception(f"Queue is full (max {self.max_queue_size})")

        operation_id = str(uuid.uuid4())
        now = datetime.now()

        operation = QueuedOperation(
            id=operation_id,
            operation_type=operation_type,
            timestamp=now.isoformat(),
            status=OperationStatus.PENDING,
            priority=priority,
            max_retries=max_retries or self.default_max_retries,
            retry_count=0,
            retry_delay=retry_delay or self.default_retry_delay,
            next_retry=now.isoformat(),
            data=data,
        )

        self.operations.append(operation)
        self.operations.sort(
            key=lambda x: x.priority, reverse=True
        )  # High priority first

        self.save_queue()

        logger.info(f"Enqueued {operation_type.value} operation: {operation_id}")

        # Try to process immediately if online
        if self.network_monitor.is_online():
            self.start_processing()

        return operation_id

    def _cleanup_completed_operations(self, keep_recent: int = 100):
        """Remove old completed operations"""
        # Keep recent completed operations for history
        completed_ops = [
            op for op in self.operations if op.status == OperationStatus.COMPLETED
        ]

        if len(completed_ops) > keep_recent:
            # Sort by timestamp and keep only recent ones
            completed_ops.sort(key=lambda x: x.timestamp, reverse=True)
            old_ops = completed_ops[keep_recent:]

            # Remove old operations
            for old_op in old_ops:
                self.operations.remove(old_op)

            logger.info(f"Cleaned up {len(old_ops)} old completed operations")

    def get_operation_status(self, operation_id: str) -> Optional[QueuedOperation]:
        """Get status of specific operation"""
        for operation in self.operations:
            if operation.id == operation_id:
                return operation
        return None

    def cancel_operation(self, operation_id: str) -> bool:
        """Cancel pending operation"""
        for operation in self.operations:
            if operation.id == operation_id:
                if operation.status in [
                    OperationStatus.PENDING,
                    OperationStatus.RETRYING,
                ]:
                    operation.status = OperationStatus.CANCELLED
                    self.save_queue()
                    logger.info(f"Cancelled operation: {operation_id}")
                    return True
                else:
                    logger.warning(
                        f"Cannot cancel operation in status: {operation.status}"
                    )
                    return False
        return False

    def start_processing(self):
        """Start processing queue in background thread"""
        if self.processing:
            logger.debug("Queue processing already running")
            return

        self.processing = True
        self.processor_thread = threading.Thread(
            target=self._process_queue, daemon=True
        )
        self.processor_thread.start()
        logger.info("Started queue processing")

    def stop_processing(self):
        """Stop processing queue"""
        self.processing = False
        if self.processor_thread:
            self.processor_thread.join(timeout=5)
        logger.info("Stopped queue processing")

    def _process_queue(self):
        """Process operations in the queue"""
        logger.info("Queue processor started")

        while self.processing:
            try:
                # Check network connectivity
                if not self.network_monitor.is_online():
                    logger.debug("Network unavailable, waiting...")
                    time.sleep(30)  # Wait 30 seconds before checking again
                    continue

                # Find next operation to process
                operation = self._get_next_operation()

                if not operation:
                    time.sleep(10)  # No operations ready, wait 10 seconds
                    continue

                # Process the operation
                self._process_operation(operation)

            except Exception as e:
                logger.error(f"Error in queue processor: {e}")
                time.sleep(10)

        logger.info("Queue processor stopped")

    def _get_next_operation(self) -> Optional[QueuedOperation]:
        """Get next operation ready for processing"""
        now = datetime.now()

        for operation in self.operations:
            if operation.status in [OperationStatus.PENDING, OperationStatus.RETRYING]:
                next_retry = datetime.fromisoformat(operation.next_retry)
                if now >= next_retry:
                    return operation

        return None

    def _process_operation(self, operation: QueuedOperation):
        """Process a single operation"""
        logger.info(
            f"Processing operation: {operation.id} ({operation.operation_type.value})"
        )

        operation.status = OperationStatus.PROCESSING
        self.save_queue()

        try:
            # Get handler for operation type
            handler = self.operation_handlers.get(operation.operation_type)

            if not handler:
                raise Exception(
                    f"No handler registered for {operation.operation_type.value}"
                )

            # Execute operation
            result = handler(operation.data)

            # Mark as completed
            operation.status = OperationStatus.COMPLETED
            operation.result = result

            logger.info(f"Operation completed successfully: {operation.id}")

        except Exception as e:
            error_msg = str(e)
            logger.error(f"Operation failed: {operation.id} - {error_msg}")

            operation.error = error_msg
            operation.retry_count += 1

            if operation.retry_count < operation.max_retries:
                # Schedule retry
                next_retry = datetime.now() + timedelta(seconds=operation.retry_delay)
                operation.next_retry = next_retry.isoformat()
                operation.status = OperationStatus.RETRYING

                logger.info(
                    f"Scheduled retry {operation.retry_count}/{operation.max_retries} for {operation.id}"
                )
            else:
                # Max retries reached
                operation.status = OperationStatus.FAILED
                logger.error(f"Operation failed permanently: {operation.id}")

        self.save_queue()

    def get_queue_stats(self) -> dict:
        """Get queue statistics"""
        stats = {
            "total_operations": len(self.operations),
            "pending": 0,
            "processing": 0,
            "completed": 0,
            "failed": 0,
            "retrying": 0,
            "cancelled": 0,
            "by_type": {},
            "network_online": self.network_monitor.is_online(),
            "processing_active": self.processing,
        }

        for operation in self.operations:
            status_key = operation.status.value
            stats[status_key] += 1

            op_type = operation.operation_type.value
            if op_type not in stats["by_type"]:
                stats["by_type"][op_type] = 0
            stats["by_type"][op_type] += 1

        return stats

    def get_recent_operations(self, limit: int = 50) -> List[dict]:
        """Get recent operations for monitoring"""
        sorted_ops = sorted(self.operations, key=lambda x: x.timestamp, reverse=True)
        return [op.to_dict() for op in sorted_ops[:limit]]

    def force_retry_failed(self) -> int:
        """Force retry all failed operations"""
        retry_count = 0

        for operation in self.operations:
            if operation.status == OperationStatus.FAILED:
                operation.status = OperationStatus.PENDING
                operation.retry_count = 0
                operation.next_retry = datetime.now().isoformat()
                operation.error = None
                retry_count += 1

        if retry_count > 0:
            self.save_queue()
            logger.info(f"Reset {retry_count} failed operations for retry")

        return retry_count

    def clear_completed_operations(self, older_than_days: int = 7) -> int:
        """Clear completed operations older than specified days"""
        cutoff_date = datetime.now() - timedelta(days=older_than_days)
        removed_count = 0

        self.operations = [
            op
            for op in self.operations
            if not (
                op.status == OperationStatus.COMPLETED
                and datetime.fromisoformat(op.timestamp) < cutoff_date
            )
        ]

        if removed_count > 0:
            self.save_queue()
            logger.info(f"Cleared {removed_count} old completed operations")

        return removed_count


# Example handlers for common operations
class DefaultOperationHandlers:
    """Default operation handlers for common NIMDA operations"""

    @staticmethod
    def git_sync_handler(data: dict) -> dict:
        """Handle git sync operations"""
        # This would integrate with GitManager
        logger.info("Executing git sync operation")
        # Placeholder implementation
        return {"success": True, "message": "Git sync completed"}

    @staticmethod
    def git_push_handler(data: dict) -> dict:
        """Handle git push operations"""
        logger.info("Executing git push operation")
        # Placeholder implementation
        return {"success": True, "message": "Git push completed"}

    @staticmethod
    def codex_sync_handler(data: dict) -> dict:
        """Handle codex sync operations"""
        logger.info("Executing codex sync operation")
        # Placeholder implementation
        return {"success": True, "message": "Codex sync completed"}


def main():
    """Example usage and testing"""
    print("🔄 NIMDA Offline Queue System")
    print("=" * 40)

    # Initialize queue
    queue = OfflineQueue()

    # Register default handlers
    handlers = DefaultOperationHandlers()
    queue.register_handler(OperationType.GIT_SYNC, handlers.git_sync_handler)
    queue.register_handler(OperationType.GIT_PUSH, handlers.git_push_handler)
    queue.register_handler(OperationType.CODEX_SYNC, handlers.codex_sync_handler)

    # Example operations
    operations = [
        {
            "type": OperationType.GIT_SYNC,
            "data": {"repository": "main", "branch": "master"},
            "priority": 10,
        },
        {
            "type": OperationType.CODEX_SYNC,
            "data": {"sync_type": "full"},
            "priority": 8,
        },
        {
            "type": OperationType.GIT_PUSH,
            "data": {"branch": "master", "message": "Auto commit"},
            "priority": 7,
        },
    ]

    # Add operations to queue
    operation_ids = []
    for op in operations:
        op_id = queue.enqueue_operation(
            operation_type=op["type"], data=op["data"], priority=op["priority"]
        )
        operation_ids.append(op_id)
        print(f"✅ Enqueued {op['type'].value}: {op_id}")

    # Start processing
    queue.start_processing()

    # Show stats
    print("\n📊 Queue Statistics:")
    stats = queue.get_queue_stats()
    for key, value in stats.items():
        if key != "by_type":
            print(f"  {key}: {value}")

    print("\n📋 Operations by type:")
    for op_type, count in stats["by_type"].items():
        print(f"  {op_type}: {count}")

    # Monitor for a bit
    print("\n🔍 Monitoring operations...")
    for i in range(10):
        time.sleep(2)
        current_stats = queue.get_queue_stats()
        processing = current_stats["processing"]
        completed = current_stats["completed"]
        failed = current_stats["failed"]

        print(
            f"  Step {i + 1}: Processing={processing}, Completed={completed}, Failed={failed}"
        )

        if completed + failed >= len(operations):
            break

    # Final stats
    print("\n📊 Final Statistics:")
    final_stats = queue.get_queue_stats()
    for key, value in final_stats.items():
        if key != "by_type":
            print(f"  {key}: {value}")

    # Stop processing
    queue.stop_processing()
    print("\n✅ Queue processing stopped")


if __name__ == "__main__":
    main()
