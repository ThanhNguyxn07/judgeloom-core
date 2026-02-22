from __future__ import annotations

from threading import Lock
from typing import Any

from apps.submissions.constants import SubmissionStatus


class BridgeManager:
    """Singleton registry and dispatcher for connected judge handlers."""

    _instance: BridgeManager | None = None
    _instance_lock: Lock = Lock()

    def __init__(self) -> None:
        """Initialize internal handler registry."""
        self._handlers: dict[str, Any] = {}
        self._handlers_lock = Lock()

    @classmethod
    def get_instance(cls) -> BridgeManager:
        """Return the singleton bridge manager instance.

        Returns:
            Shared manager instance.
        """
        if cls._instance is None:
            with cls._instance_lock:
                if cls._instance is None:
                    cls._instance = cls()
        return cls._instance

    def register_judge(self, handler: Any) -> None:
        """Register a connected judge handler.

        Args:
            handler: JudgeHandler instance.
        """
        judge = getattr(handler, "judge", None)
        if judge is None:
            return
        with self._handlers_lock:
            self._handlers[judge.name] = handler

    def unregister_judge(self, handler: Any) -> None:
        """Unregister a judge handler.

        Args:
            handler: JudgeHandler instance.
        """
        judge = getattr(handler, "judge", None)
        if judge is None:
            return
        with self._handlers_lock:
            self._handlers.pop(judge.name, None)

    def get_available_judge(self, problem: Any, language: Any) -> Any | None:
        """Pick the best available judge for a submission.

        Args:
            problem: Problem instance to judge.
            language: Language instance requested.

        Returns:
            Best-fit JudgeHandler or None.
        """
        candidates: list[Any] = []

        with self._handlers_lock:
            handlers = list(self._handlers.values())

        for handler in handlers:
            judge = getattr(handler, "judge", None)
            if judge is None:
                continue
            if not judge.online or judge.is_blocked:
                continue
            if not judge.runtimes.filter(id=language.id).exists():
                continue

            has_cached_problems = judge.problems.exists()
            if has_cached_problems and not judge.problems.filter(id=problem.id).exists():
                continue

            candidates.append(handler)

        if not candidates:
            return None

        return min(candidates, key=lambda item: getattr(item.judge, "load", 0.0) or 0.0)

    def dispatch_submission(self, submission: Any) -> bool:
        """Dispatch a submission to an available judge.

        Args:
            submission: Submission instance.

        Returns:
            True if dispatch succeeded.
        """
        handler = self.get_available_judge(problem=submission.problem, language=submission.language)
        if handler is None:
            return False

        source_code = ""
        source_obj = getattr(submission, "source", None)
        if source_obj is not None:
            source_code = source_obj.source_code

        payload = {
            "submission_id": submission.id,
            "problem_id": submission.problem_id,
            "language_id": submission.language_id,
            "language_key": submission.language.key,
            "source_code": source_code,
            "time_limit": getattr(submission.problem, "time_limit", None),
            "memory_limit": getattr(submission.problem, "memory_limit", None),
        }

        dispatched = handler.send_submission(payload)
        if not dispatched:
            return False

        submission.status = SubmissionStatus.COMPILING
        submission.judged_on = handler.judge
        submission.save(update_fields=["status", "judged_on", "updated_at"])
        return True

    def get_connected_judges(self) -> list[dict[str, Any]]:
        """Return lightweight state for connected judges.

        Returns:
            List of judge snapshots.
        """
        with self._handlers_lock:
            handlers = list(self._handlers.values())

        snapshots: list[dict[str, Any]] = []
        for handler in handlers:
            judge = getattr(handler, "judge", None)
            if judge is None:
                continue
            snapshots.append(
                {
                    "name": judge.name,
                    "online": judge.online,
                    "is_blocked": judge.is_blocked,
                    "ping": judge.ping,
                    "load": judge.load,
                    "status": judge.status,
                }
            )
        return snapshots
