#!/usr/bin/env python3
"""
Advanced Backup Rotation System for NIMDA Agent
Provides automated backup creation, rotation, and verification
"""

import hashlib
import json
import logging
import shutil
import subprocess
import threading
import time
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional

# Setup logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class BackupType(Enum):
    """Types of backups"""

    FULL = "full"
    INCREMENTAL = "incremental"
    DIFFERENTIAL = "differential"
    SNAPSHOT = "snapshot"
    GIT_BUNDLE = "git_bundle"


class BackupStatus(Enum):
    """Backup operation status"""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CORRUPTED = "corrupted"
    VERIFIED = "verified"


@dataclass
class BackupMetadata:
    """Metadata for a backup"""

    backup_id: str
    timestamp: str
    backup_type: BackupType
    size_bytes: int
    checksum: str
    file_count: int
    source_path: str
    backup_path: str
    status: BackupStatus
    verification_date: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[List[str]] = None


class BackupRotationPolicy:
    """Backup retention policy"""

    def __init__(self):
        # Keep backups for different time periods
        self.hourly_keep = 24  # Keep 24 hourly backups (1 day)
        self.daily_keep = 30  # Keep 30 daily backups (1 month)
        self.weekly_keep = 12  # Keep 12 weekly backups (3 months)
        self.monthly_keep = 12  # Keep 12 monthly backups (1 year)

        # Size limits
        self.max_total_size_gb = 10  # Maximum total backup size
        self.max_backup_count = 100  # Maximum number of backups

        # Automatic cleanup
        self.auto_cleanup = True
        self.verify_before_delete = True


class BackupManager:
    """Advanced backup manager with rotation and verification"""

    def __init__(self, backup_root: str = ".nimda_backups"):
        self.backup_root = Path(backup_root)
        self.backup_root.mkdir(exist_ok=True)

        # Subdirectories
        self.full_backups_dir = self.backup_root / "full"
        self.incremental_backups_dir = self.backup_root / "incremental"
        self.snapshots_dir = self.backup_root / "snapshots"
        self.git_bundles_dir = self.backup_root / "git_bundles"

        # Create subdirectories
        for dir_path in [
            self.full_backups_dir,
            self.incremental_backups_dir,
            self.snapshots_dir,
            self.git_bundles_dir,
        ]:
            dir_path.mkdir(exist_ok=True)

        # Metadata storage
        self.metadata_file = self.backup_root / "backup_metadata.json"
        self.metadata: List[BackupMetadata] = self.load_metadata()

        # Rotation policy
        self.rotation_policy = BackupRotationPolicy()

        # Background tasks
        self.monitor_thread = None
        self.monitoring = False

    def load_metadata(self) -> List[BackupMetadata]:
        """Load backup metadata from file"""
        try:
            if self.metadata_file.exists():
                with open(self.metadata_file, "r", encoding="utf-8") as f:
                    data = json.load(f)

                metadata_list = []
                for item in data.get("backups", []):
                    metadata = BackupMetadata(
                        backup_id=item["backup_id"],
                        timestamp=item["timestamp"],
                        backup_type=BackupType(item["backup_type"]),
                        size_bytes=item["size_bytes"],
                        checksum=item["checksum"],
                        file_count=item["file_count"],
                        source_path=item["source_path"],
                        backup_path=item["backup_path"],
                        status=BackupStatus(item["status"]),
                        verification_date=item.get("verification_date"),
                        description=item.get("description"),
                        tags=item.get("tags", []),
                    )
                    metadata_list.append(metadata)

                logger.info(f"Loaded {len(metadata_list)} backup records")
                return metadata_list

        except Exception as e:
            logger.error(f"Error loading backup metadata: {e}")

        return []

    def save_metadata(self):
        """Save backup metadata to file"""
        try:
            data = {
                "last_updated": datetime.now().isoformat(),
                "policy": {
                    "hourly_keep": self.rotation_policy.hourly_keep,
                    "daily_keep": self.rotation_policy.daily_keep,
                    "weekly_keep": self.rotation_policy.weekly_keep,
                    "monthly_keep": self.rotation_policy.monthly_keep,
                    "max_total_size_gb": self.rotation_policy.max_total_size_gb,
                    "max_backup_count": self.rotation_policy.max_backup_count,
                },
                "backups": [],
            }

            for metadata in self.metadata:
                backup_data = {
                    "backup_id": metadata.backup_id,
                    "timestamp": metadata.timestamp,
                    "backup_type": metadata.backup_type.value,
                    "size_bytes": metadata.size_bytes,
                    "checksum": metadata.checksum,
                    "file_count": metadata.file_count,
                    "source_path": metadata.source_path,
                    "backup_path": metadata.backup_path,
                    "status": metadata.status.value,
                    "verification_date": metadata.verification_date,
                    "description": metadata.description,
                    "tags": metadata.tags or [],
                }
                data["backups"].append(backup_data)

            with open(self.metadata_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

        except Exception as e:
            logger.error(f"Error saving backup metadata: {e}")

    def calculate_checksum(self, file_path: Path) -> str:
        """Calculate SHA256 checksum of file"""
        sha256_hash = hashlib.sha256()

        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256_hash.update(chunk)

        return sha256_hash.hexdigest()

    def calculate_directory_checksum(self, dir_path: Path) -> str:
        """Calculate checksum for entire directory"""
        sha256_hash = hashlib.sha256()

        for file_path in sorted(dir_path.rglob("*")):
            if file_path.is_file():
                # Include file path in hash for structure verification
                sha256_hash.update(str(file_path.relative_to(dir_path)).encode())

                with open(file_path, "rb") as f:
                    for chunk in iter(lambda: f.read(4096), b""):
                        sha256_hash.update(chunk)

        return sha256_hash.hexdigest()

    def create_full_backup(
        self,
        source_path: str,
        description: Optional[str] = None,
        tags: Optional[List[str]] = None,
    ) -> str:
        """Create full backup of source directory"""
        source = Path(source_path)
        if not source.exists():
            raise ValueError(f"Source path does not exist: {source_path}")

        # Generate backup ID and paths
        backup_id = f"full_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        backup_file = self.full_backups_dir / f"{backup_id}.tar.gz"

        logger.info(f"Creating full backup: {backup_id}")

        try:
            # Create compressed archive
            subprocess.run(
                [
                    "tar",
                    "-czf",
                    str(backup_file),
                    "-C",
                    str(source.parent),
                    source.name,
                ],
                check=True,
                capture_output=True,
            )

            # Calculate metadata
            file_count = sum(1 for _ in source.rglob("*") if _.is_file())
            size_bytes = backup_file.stat().st_size
            checksum = self.calculate_checksum(backup_file)

            # Create metadata
            metadata = BackupMetadata(
                backup_id=backup_id,
                timestamp=datetime.now().isoformat(),
                backup_type=BackupType.FULL,
                size_bytes=size_bytes,
                checksum=checksum,
                file_count=file_count,
                source_path=str(source),
                backup_path=str(backup_file),
                status=BackupStatus.COMPLETED,
                description=description,
                tags=tags or [],
            )

            self.metadata.append(metadata)
            self.save_metadata()

            logger.info(f"Full backup completed: {backup_id} ({size_bytes:,} bytes)")
            return backup_id

        except Exception as e:
            logger.error(f"Error creating full backup: {e}")
            # Clean up failed backup
            if backup_file.exists():
                backup_file.unlink()
            raise

    def create_git_bundle_backup(
        self, repo_path: str, description: Optional[str] = None
    ) -> str:
        """Create Git bundle backup"""
        repo = Path(repo_path)
        if not (repo / ".git").exists():
            raise ValueError(f"Not a Git repository: {repo_path}")

        backup_id = f"git_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        bundle_file = self.git_bundles_dir / f"{backup_id}.bundle"

        logger.info(f"Creating Git bundle backup: {backup_id}")

        try:
            # Create Git bundle with all refs
            subprocess.run(
                ["git", "-C", str(repo), "bundle", "create", str(bundle_file), "--all"],
                check=True,
                capture_output=True,
            )

            # Calculate metadata
            size_bytes = bundle_file.stat().st_size
            checksum = self.calculate_checksum(bundle_file)

            # Get commit count
            result = subprocess.run(
                ["git", "-C", str(repo), "rev-list", "--all", "--count"],
                check=True,
                capture_output=True,
                text=True,
            )
            commit_count = int(result.stdout.strip())

            metadata = BackupMetadata(
                backup_id=backup_id,
                timestamp=datetime.now().isoformat(),
                backup_type=BackupType.GIT_BUNDLE,
                size_bytes=size_bytes,
                checksum=checksum,
                file_count=commit_count,  # Using commit count as file count
                source_path=str(repo),
                backup_path=str(bundle_file),
                status=BackupStatus.COMPLETED,
                description=description or "Git repository bundle",
                tags=["git", "bundle"],
            )

            self.metadata.append(metadata)
            self.save_metadata()

            logger.info(
                f"Git bundle backup completed: {backup_id} ({size_bytes:,} bytes)"
            )
            return backup_id

        except Exception as e:
            logger.error(f"Error creating Git bundle backup: {e}")
            if bundle_file.exists():
                bundle_file.unlink()
            raise

    def create_snapshot_backup(
        self, source_path: str, description: Optional[str] = None
    ) -> str:
        """Create snapshot backup (copy without compression)"""
        source = Path(source_path)
        if not source.exists():
            raise ValueError(f"Source path does not exist: {source_path}")

        backup_id = f"snapshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        snapshot_dir = self.snapshots_dir / backup_id

        logger.info(f"Creating snapshot backup: {backup_id}")

        try:
            # Copy directory structure
            shutil.copytree(
                source,
                snapshot_dir,
                ignore=shutil.ignore_patterns("*.pyc", "__pycache__", ".git"),
            )

            # Calculate metadata
            file_count = sum(1 for _ in snapshot_dir.rglob("*") if _.is_file())
            size_bytes = sum(
                f.stat().st_size for f in snapshot_dir.rglob("*") if f.is_file()
            )
            checksum = self.calculate_directory_checksum(snapshot_dir)

            metadata = BackupMetadata(
                backup_id=backup_id,
                timestamp=datetime.now().isoformat(),
                backup_type=BackupType.SNAPSHOT,
                size_bytes=size_bytes,
                checksum=checksum,
                file_count=file_count,
                source_path=str(source),
                backup_path=str(snapshot_dir),
                status=BackupStatus.COMPLETED,
                description=description,
                tags=["snapshot"],
            )

            self.metadata.append(metadata)
            self.save_metadata()

            logger.info(
                f"Snapshot backup completed: {backup_id} ({size_bytes:,} bytes)"
            )
            return backup_id

        except Exception as e:
            logger.error(f"Error creating snapshot backup: {e}")
            if snapshot_dir.exists():
                shutil.rmtree(snapshot_dir)
            raise

    def verify_backup(self, backup_id: str) -> bool:
        """Verify backup integrity"""
        metadata = self.get_backup_metadata(backup_id)
        if not metadata:
            logger.error(f"Backup metadata not found: {backup_id}")
            return False

        backup_path = Path(metadata.backup_path)
        if not backup_path.exists():
            logger.error(f"Backup file not found: {backup_path}")
            metadata.status = BackupStatus.CORRUPTED
            self.save_metadata()
            return False

        logger.info(f"Verifying backup: {backup_id}")

        try:
            # Calculate current checksum
            if metadata.backup_type == BackupType.SNAPSHOT:
                current_checksum = self.calculate_directory_checksum(backup_path)
            else:
                current_checksum = self.calculate_checksum(backup_path)

            # Compare with stored checksum
            if current_checksum == metadata.checksum:
                metadata.status = BackupStatus.VERIFIED
                metadata.verification_date = datetime.now().isoformat()
                self.save_metadata()
                logger.info(f"Backup verification successful: {backup_id}")
                return True
            else:
                metadata.status = BackupStatus.CORRUPTED
                self.save_metadata()
                logger.error(
                    f"Backup verification failed: {backup_id} (checksum mismatch)"
                )
                return False

        except Exception as e:
            logger.error(f"Error verifying backup {backup_id}: {e}")
            return False

    def get_backup_metadata(self, backup_id: str) -> Optional[BackupMetadata]:
        """Get metadata for specific backup"""
        for metadata in self.metadata:
            if metadata.backup_id == backup_id:
                return metadata
        return None

    def list_backups(
        self, backup_type: Optional[BackupType] = None, tags: Optional[List[str]] = None
    ) -> List[BackupMetadata]:
        """List backups with optional filtering"""
        filtered_backups = self.metadata

        if backup_type:
            filtered_backups = [
                b for b in filtered_backups if b.backup_type == backup_type
            ]

        if tags:
            filtered_backups = [
                b
                for b in filtered_backups
                if b.tags and any(tag in b.tags for tag in tags)
            ]

        return sorted(filtered_backups, key=lambda x: x.timestamp, reverse=True)

    def restore_backup(self, backup_id: str, restore_path: str) -> bool:
        """Restore backup to specified location"""
        metadata = self.get_backup_metadata(backup_id)
        if not metadata:
            logger.error(f"Backup not found: {backup_id}")
            return False

        backup_path = Path(metadata.backup_path)
        restore_location = Path(restore_path)

        logger.info(f"Restoring backup {backup_id} to {restore_path}")

        try:
            if metadata.backup_type == BackupType.FULL:
                # Extract tar.gz
                subprocess.run(
                    [
                        "tar",
                        "-xzf",
                        str(backup_path),
                        "-C",
                        str(restore_location.parent),
                    ],
                    check=True,
                )

            elif metadata.backup_type == BackupType.SNAPSHOT:
                # Copy directory
                if restore_location.exists():
                    shutil.rmtree(restore_location)
                shutil.copytree(backup_path, restore_location)

            elif metadata.backup_type == BackupType.GIT_BUNDLE:
                # Clone from bundle
                subprocess.run(
                    ["git", "clone", str(backup_path), str(restore_location)],
                    check=True,
                )

            logger.info(f"Backup restoration completed: {backup_id}")
            return True

        except Exception as e:
            logger.error(f"Error restoring backup {backup_id}: {e}")
            return False

    def apply_rotation_policy(self) -> Dict[str, int]:
        """Apply backup rotation policy"""
        logger.info("Applying backup rotation policy")

        now = datetime.now()
        stats = {"removed": 0, "kept": 0, "total_size_freed": 0}

        # Group backups by time periods
        backups_to_keep = set()

        # Keep recent backups based on policy
        for metadata in sorted(self.metadata, key=lambda x: x.timestamp, reverse=True):
            backup_time = datetime.fromisoformat(metadata.timestamp)
            age = now - backup_time

            # Always keep recent backups (last 24 hours)
            if age < timedelta(hours=24):
                backups_to_keep.add(metadata.backup_id)
                continue

            # Weekly backups (keep every 7 days)
            if age < timedelta(weeks=self.rotation_policy.weekly_keep):
                if backup_time.weekday() == 0:  # Monday
                    backups_to_keep.add(metadata.backup_id)
                continue

            # Monthly backups (keep first of month)
            if age < timedelta(days=self.rotation_policy.monthly_keep * 30):
                if backup_time.day == 1:
                    backups_to_keep.add(metadata.backup_id)
                continue

        # Remove old backups
        for metadata in self.metadata[:]:  # Copy list to modify during iteration
            if metadata.backup_id not in backups_to_keep:
                if self.remove_backup(metadata.backup_id, verify_first=True):
                    stats["removed"] += 1
                    stats["total_size_freed"] += metadata.size_bytes
            else:
                stats["kept"] += 1

        # Apply size limit
        total_size = sum(m.size_bytes for m in self.metadata)
        if total_size > self.rotation_policy.max_total_size_gb * 1024**3:
            # Remove oldest backups until under limit
            sorted_backups = sorted(self.metadata, key=lambda x: x.timestamp)
            for metadata in sorted_backups:
                if total_size <= self.rotation_policy.max_total_size_gb * 1024**3:
                    break
                if self.remove_backup(metadata.backup_id):
                    total_size -= metadata.size_bytes
                    stats["removed"] += 1
                    stats["total_size_freed"] += metadata.size_bytes

        logger.info(f"Rotation policy applied: {stats}")
        return stats

    def remove_backup(self, backup_id: str, verify_first: bool = True) -> bool:
        """Remove backup and its metadata"""
        metadata = self.get_backup_metadata(backup_id)
        if not metadata:
            return False

        # Verify backup before deletion if requested
        if verify_first and metadata.status != BackupStatus.CORRUPTED:
            if not self.verify_backup(backup_id):
                logger.warning(
                    f"Backup {backup_id} failed verification, removing anyway"
                )

        try:
            backup_path = Path(metadata.backup_path)
            if backup_path.exists():
                if backup_path.is_dir():
                    shutil.rmtree(backup_path)
                else:
                    backup_path.unlink()

            # Remove from metadata
            self.metadata = [m for m in self.metadata if m.backup_id != backup_id]
            self.save_metadata()

            logger.info(f"Removed backup: {backup_id}")
            return True

        except Exception as e:
            logger.error(f"Error removing backup {backup_id}: {e}")
            return False

    def get_backup_stats(self) -> dict:
        """Get backup statistics"""
        total_size = sum(m.size_bytes for m in self.metadata)
        by_type = {}
        by_status = {}

        for metadata in self.metadata:
            # Count by type
            type_key = metadata.backup_type.value
            if type_key not in by_type:
                by_type[type_key] = {"count": 0, "size": 0}
            by_type[type_key]["count"] += 1
            by_type[type_key]["size"] += metadata.size_bytes

            # Count by status
            status_key = metadata.status.value
            by_status[status_key] = by_status.get(status_key, 0) + 1

        return {
            "total_backups": len(self.metadata),
            "total_size_bytes": total_size,
            "total_size_gb": total_size / (1024**3),
            "by_type": by_type,
            "by_status": by_status,
            "oldest_backup": min(self.metadata, key=lambda x: x.timestamp).timestamp
            if self.metadata
            else None,
            "newest_backup": max(self.metadata, key=lambda x: x.timestamp).timestamp
            if self.metadata
            else None,
        }

    def start_monitoring(self, check_interval: int = 3600):
        """Start background monitoring and maintenance"""
        if self.monitoring:
            return

        self.monitoring = True
        self.monitor_thread = threading.Thread(
            target=self._monitoring_loop, args=(check_interval,), daemon=True
        )
        self.monitor_thread.start()
        logger.info("Started backup monitoring")

    def stop_monitoring(self):
        """Stop background monitoring"""
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)
        logger.info("Stopped backup monitoring")

    def _monitoring_loop(self, check_interval: int):
        """Background monitoring loop"""
        while self.monitoring:
            try:
                # Apply rotation policy
                if self.rotation_policy.auto_cleanup:
                    self.apply_rotation_policy()

                # Verify random backups
                unverified_backups = [
                    m
                    for m in self.metadata
                    if m.status == BackupStatus.COMPLETED and not m.verification_date
                ]

                if unverified_backups:
                    # Verify one random backup
                    import random

                    backup_to_verify = random.choice(unverified_backups)
                    self.verify_backup(backup_to_verify.backup_id)

                time.sleep(check_interval)

            except Exception as e:
                logger.error(f"Error in backup monitoring: {e}")
                time.sleep(60)  # Wait 1 minute before retrying


def main():
    """Example usage and testing"""
    print("💾 NIMDA Advanced Backup System")
    print("=" * 40)

    # Initialize backup manager
    backup_manager = BackupManager()

    # Get current directory for testing
    test_source = Path.cwd()

    print(f"📁 Test source: {test_source}")

    # Create different types of backups
    try:
        # Create full backup
        print("\n🔄 Creating full backup...")
        full_backup_id = backup_manager.create_full_backup(
            str(test_source), description="Test full backup", tags=["test", "full"]
        )
        print(f"✅ Full backup created: {full_backup_id}")

        # Create snapshot backup (if not too large)
        total_size = sum(
            f.stat().st_size for f in test_source.rglob("*") if f.is_file()
        )
        if total_size < 100 * 1024 * 1024:  # Less than 100MB
            print("\n📸 Creating snapshot backup...")
            snapshot_backup_id = backup_manager.create_snapshot_backup(
                str(test_source), description="Test snapshot backup"
            )
            print(f"✅ Snapshot backup created: {snapshot_backup_id}")

        # Create Git bundle if it's a Git repo
        if (test_source / ".git").exists():
            print("\n🔗 Creating Git bundle backup...")
            git_backup_id = backup_manager.create_git_bundle_backup(
                str(test_source), description="Test Git bundle backup"
            )
            print(f"✅ Git bundle backup created: {git_backup_id}")

        # Verify backups
        print("\n🔍 Verifying backups...")
        for backup in backup_manager.list_backups():
            is_valid = backup_manager.verify_backup(backup.backup_id)
            status = "✅ Valid" if is_valid else "❌ Invalid"
            print(f"  {backup.backup_id}: {status}")

        # Show statistics
        print("\n📊 Backup Statistics:")
        stats = backup_manager.get_backup_stats()
        print(f"  Total backups: {stats['total_backups']}")
        print(f"  Total size: {stats['total_size_gb']:.2f} GB")
        print(f"  By type: {stats['by_type']}")
        print(f"  By status: {stats['by_status']}")

        # Test rotation policy
        print("\n🔄 Testing rotation policy...")
        rotation_stats = backup_manager.apply_rotation_policy()
        print(f"  Backups removed: {rotation_stats['removed']}")
        print(f"  Backups kept: {rotation_stats['kept']}")
        print(f"  Space freed: {rotation_stats['total_size_freed'] / (1024**2):.2f} MB")

    except Exception as e:
        print(f"❌ Error: {e}")

    print("\n✅ Backup system test completed")


if __name__ == "__main__":
    main()
