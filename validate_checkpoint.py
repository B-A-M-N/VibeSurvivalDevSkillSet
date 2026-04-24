#!/usr/bin/env python3
"""
Vibe Continuity - Checkpoint Validation Script
Version: 2.1.0
Purpose: Validate checkpoint.json integrity before restoration
Usage: python3 ~/.vibe/scripts/validate_checkpoint.py [path]
"""

import json
import sys
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional


class CheckpointValidator:
    """Validates checkpoint files for Vibe Continuity Framework."""
    
    REQUIRED_FIELDS = [
        "task",
        "execution", 
        "next_step",
        "completed_steps",
        "session"
    ]
    
    NEXT_STEP_REQUIRED = [
        "id",
        "description", 
        "action_type",
        "target",
        "expected_outcome"
    ]
    
    TASK_REQUIRED = [
        "id",
        "objective",
        "created_at",
        "updated_at"
    ]
    
    EXECUTION_REQUIRED = [
        "phase",
        "phase_entered_at",
        "phase_reason"
    ]
    
    VALID_PHASES = [
        "INIT", "PLANNING", "EXECUTING", "BLOCKED", 
        "VERIFYING", "COMPLETE", "FAILED"
    ]
    
    VALID_ACTION_TYPES = [
        "create_file", "modify_file", "delete_file",
        "run_command", "verify", "read_file", "checkpoint_only"
    ]
    
    def __init__(self, checkpoint_path: str = ".checkpoint.json"):
        self.checkpoint_path = checkpoint_path
        self.checkpoint: Optional[Dict[str, Any]] = None
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.info: List[str] = []
    
    def load_checkpoint(self) -> bool:
        """Load and parse the checkpoint file."""
        try:
            with open(self.checkpoint_path, 'r') as f:
                self.checkpoint = json.load(f)
            self.info.append(f"✅ Loaded checkpoint: {self.checkpoint_path}")
            return True
        except FileNotFoundError:
            self.errors.append(f"❌ Checkpoint file not found: {self.checkpoint_path}")
            return False
        except json.JSONDecodeError as e:
            self.errors.append(f"❌ Invalid JSON: {e}")
            return False
        except Exception as e:
            self.errors.append(f"❌ Unexpected error loading file: {e}")
            return False
    
    def validate_structure(self) -> bool:
        """Validate basic checkpoint structure."""
        if not self.checkpoint:
            self.errors.append("❌ No checkpoint loaded to validate")
            return False
        
        # Check required top-level fields
        for field in self.REQUIRED_FIELDS:
            if field not in self.checkpoint:
                self.errors.append(f"❌ Missing required field: {field}")
        
        # Check schema version if present
        schema_version = self.checkpoint.get("schema_version", "2.0.0")
        self.info.append(f"📋 Schema version: {schema_version}")
        
        return len(self.errors) == 0
    
    def validate_task(self) -> bool:
        """Validate task section."""
        if "task" not in self.checkpoint:
            return False
        
        task = self.checkpoint["task"]
        if not isinstance(task, dict):
            self.errors.append("❌ task must be a dictionary")
            return False
        
        for field in self.TASK_REQUIRED:
            if field not in task:
                self.errors.append(f"❌ task missing required field: {field}")
        
        # Validate task.id format
        task_id = task.get("id", "")
        if not task_id or len(task_id) > 100:
            self.warnings.append(f"⚠️  task.id may be invalid: {task_id}")
        
        # Validate dates are ISO8601
        for date_field in ["created_at", "updated_at"]:
            if date_field in task:
                date_str = task[date_field]
                try:
                    datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                except ValueError:
                    self.warnings.append(f"⚠️  task.{date_field} not valid ISO8601: {date_str}")
        
        self.info.append(f"📋 Task: {task_id} - {task.get('objective', 'N/A')}")
        return len(self.errors) == 0
    
    def validate_execution(self) -> bool:
        """Validate execution section."""
        if "execution" not in self.checkpoint:
            return False
        
        execution = self.checkpoint["execution"]
        if not isinstance(execution, dict):
            self.errors.append("❌ execution must be a dictionary")
            return False
        
        for field in self.EXECUTION_REQUIRED:
            if field not in execution:
                self.errors.append(f"❌ execution missing required field: {field}")
        
        # Validate phase
        phase = execution.get("phase", "")
        if phase not in self.VALID_PHASES:
            self.errors.append(f"❌ Invalid phase: {phase}. Must be one of: {', '.join(self.VALID_PHASES)}")
        else:
            self.info.append(f"📊 Phase: {phase}")
        
        return len(self.errors) == 0
    
    def validate_next_step(self) -> bool:
        """Validate next_step section."""
        if "next_step" not in self.checkpoint:
            self.errors.append("❌ Missing next_step field")
            return False
        
        next_step = self.checkpoint["next_step"]
        if not isinstance(next_step, dict):
            self.errors.append("❌ next_step must be a dictionary")
            return False
        
        # Check required fields
        for field in self.NEXT_STEP_REQUIRED:
            if field not in next_step:
                self.errors.append(f"❌ next_step missing required field: {field}")
        
        # Validate action_type
        action_type = next_step.get("action_type", "")
        if action_type not in self.VALID_ACTION_TYPES:
            self.warnings.append(f"⚠️  Unrecognized action_type: {action_type}")
        
        # Validate id is numeric
        step_id = next_step.get("id", "")
        try:
            int(step_id)
            self.info.append(f"🎯 Next step: {step_id} - {next_step.get('description', 'N/A')}")
        except ValueError:
            self.warnings.append(f"⚠️  next_step.id should be numeric: {step_id}")
        
        return len(self.errors) == 0
    
    def validate_completed_steps(self) -> bool:
        """Validate completed_steps array."""
        if "completed_steps" not in self.checkpoint:
            self.errors.append("❌ Missing completed_steps field")
            return False
        
        steps = self.checkpoint["completed_steps"]
        
        if not isinstance(steps, list):
            self.errors.append("❌ completed_steps must be a list")
            return False
        
        # Validate each step has required fields
        step_required = ["id", "description", "action_type", "target", "outcome", "completed_at"]
        for i, step in enumerate(steps):
            if not isinstance(step, dict):
                self.errors.append(f"❌ completed_steps[{i}] is not a dictionary")
                continue
            
            for field in step_required:
                if field not in step:
                    self.errors.append(f"❌ completed_steps[{i}] missing: {field}")
        
        self.info.append(f"✅ {len(steps)} completed steps")
        
        # Validate step IDs are sequential and increasing
        step_ids = []
        for step in steps:
            try:
                step_ids.append(int(step.get("id", "0")))
            except ValueError:
                self.warnings.append(f"⚠️  Non-numeric step ID: {step.get('id')}")
        
        if step_ids:
            sorted_ids = sorted(step_ids)
            if step_ids != sorted_ids:
                self.warnings.append("⚠️  completed_steps IDs are not in order")
        
        return len(self.errors) == 0
    
    def validate_session(self) -> bool:
        """Validate session section."""
        if "session" not in self.checkpoint:
            self.errors.append("❌ Missing session field")
            return False
        
        session = self.checkpoint["session"]
        if not isinstance(session, dict):
            self.errors.append("❌ session must be a dictionary")
            return False
        
        # Check continuity score
        continuity_score = session.get("continuity_score", 100)
        if continuity_score < 0 or continuity_score > 100:
            self.warnings.append(f"⚠️  continuity_score out of range: {continuity_score}")
        else:
            self.info.append(f"📈 Continuity score: {continuity_score}")
        
        # Check for critical flags
        if session.get("post_compaction_resume", False):
            self.info.append("ℹ️  Post-compaction resume flag set")
        
        if session.get("dirty_resume", False):
            self.warnings.append("⚠️  Dirty resume flag set - may indicate crash")
        
        return len(self.errors) == 0
    
    def validate_no_regression(self) -> bool:
        """Validate next_step.id > max completed step id."""
        if "next_step" not in self.checkpoint or "completed_steps" not in self.checkpoint:
            return True  # Can't check if fields missing
        
        try:
            next_id = int(self.checkpoint["next_step"].get("id", "0"))
            completed_ids = []
            for step in self.checkpoint["completed_steps"]:
                completed_ids.append(int(step.get("id", "0")))
            
            if completed_ids:
                max_completed = max(completed_ids)
                if next_id <= max_completed:
                    self.errors.append(
                        f"❌ Next step ID ({next_id}) <= max completed ({max_completed}) - REGRESSION DETECTED"
                    )
                    return False
                else:
                    self.info.append(f"✅ Next step ID ({next_id}) > max completed ({max_completed})")
        except ValueError:
            self.warnings.append("⚠️  Could not validate step ID regression (non-numeric IDs)")
        
        return len(self.errors) == 0
    
    def validate_lock_file(self) -> bool:
        """Validate checkpoint lock file exists and is current."""
        lock_path = self.checkpoint_path.replace(".json", ".lock")
        
        if not os.path.exists(lock_path):
            self.warnings.append(f"⚠️  Lock file missing: {lock_path}")
            return True  # Not critical, just warning
        
        try:
            with open(lock_path, 'r') as f:
                lock_content = f.read()
            
            if lock_content.strip():
                self.info.append(f"🔒 Lock file exists")
                return True
            else:
                self.warnings.append(f"⚠️  Lock file is empty: {lock_path}")
                return True
        except Exception as e:
            self.warnings.append(f"⚠️  Could not read lock file: {e}")
            return True
    
    def validate(self) -> tuple:
        """Run all validation checks."""
        self.errors = []
        self.warnings = []
        self.info = []
        
        # Load the checkpoint
        if not self.load_checkpoint():
            return (False, self.errors, self.warnings, self.info)
        
        # Run all validations
        checks = [
            ("Structure", self.validate_structure),
            ("Task", self.validate_task),
            ("Execution", self.validate_execution),
            ("Next Step", self.validate_next_step),
            ("Completed Steps", self.validate_completed_steps),
            ("Session", self.validate_session),
            ("No Regression", self.validate_no_regression),
            ("Lock File", self.validate_lock_file),
        ]
        
        for check_name, check_func in checks:
            if not check_func():
                # Errors already added by check_func
                pass
        
        is_valid = len(self.errors) == 0
        return (is_valid, self.errors, self.warnings, self.info)
    
    def print_report(self):
        """Print validation report to console."""
        print("\n" + "=" * 70)
        print("CHECKPOINT VALIDATION REPORT")
        print("=" * 70)
        
        # Print info
        if self.info:
            print("\n📊 Info:")
            for msg in self.info:
                print(f"  {msg}")
        
        # Print warnings
        if self.warnings:
            print("\n⚠️  Warnings:")
            for msg in self.warnings:
                print(f"  {msg}")
        
        # Print errors
        if self.errors:
            print("\n❌ Errors:")
            for msg in self.errors:
                print(f"  {msg}")
        
        print("\n" + "=" * 70)
        
        if len(self.errors) == 0:
            print("✅ CHECKPOINT IS VALID")
            if len(self.warnings) > 0:
                print(f"   (with {len(self.warnings)} warnings)")
        else:
            print(f"❌ CHECKPOINT IS INVALID ({len(self.errors)} errors)")
        
        print("=" * 70 + "\n")


def main():
    """Main entry point."""
    checkpoint_path = ".checkpoint.json"
    
    # Parse command line arguments
    if len(sys.argv) > 1:
        checkpoint_path = sys.argv[1]
    
    # Handle ~ expansion
    checkpoint_path = os.path.expanduser(checkpoint_path)
    
    # Run validation
    validator = CheckpointValidator(checkpoint_path)
    is_valid, errors, warnings, info = validator.validate()
    
    # Print report
    validator.print_report()
    
    # Exit with appropriate code
    if is_valid:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
