class MultiInstanceDeadlockDetector:
    """A class to detect deadlocks in a system with multi-instance resources using the Banker's Algorithm.

    Args:
        allocation (dict): A dictionary mapping processes to their allocated resources (e.g., {'P1': {'R1': 1, 'R2': 0}}).
        max_matrix (dict): A dictionary mapping processes to their maximum resource needs.
        available (dict): A dictionary of available resource instances (e.g., {'R1': 1, 'R2': 2}).
        total_resources (dict): A dictionary of total resource instances (e.g., {'R1': 3, 'R2': 2}).

    Raises:
        ValueError: If the input data is invalid (e.g., negative values, exceeding total resources).
    """
    def __init__(self, allocation, max_matrix, available, total_resources):
        self.allocation = allocation
        self.max_matrix = max_matrix
        self.available = available
        self.total_resources = total_resources
        self.processes = list(allocation.keys())
        self._validate_input()
        self.need = self._compute_need()

    def _validate_input(self):
        """Validates the input data for consistency and correctness."""
        for p in self.processes:
            if not p.startswith("P"):
                raise ValueError(f"Invalid process name: {p}")
            for r in self.allocation[p]:
                if not r.startswith("R"):
                    raise ValueError(f"Invalid resource name: {r} in allocation for {p}")
                if self.allocation[p][r] < 0 or self.max_matrix[p][r] < 0:
                    raise ValueError(f"Negative values not allowed in allocation or max for {p}, {r}")
                if self.allocation[p][r] > self.max_matrix[p][r]:
                    raise ValueError(f"Allocation exceeds max for {p}, {r}")
                if self.max_matrix[p][r] > self.total_resources[r]:
                    raise ValueError(f"Max for {r} by {p} exceeds total instances")
        for r in self.available:
            if not r.startswith("R"):
                raise ValueError(f"Invalid resource name: {r} in available")
            if self.available[r] < 0:
                raise ValueError(f"Negative available instances for {r}")
            total_allocated = sum(self.allocation[p].get(r, 0) for p in self.processes)
            if total_allocated + self.available[r] != self.total_resources[r]:
                raise ValueError(f"Inconsistent total for {r}: allocated + available != total")

    def _compute_need(self):
        """Computes the Need matrix: Need[i][j] = Max[i][j] - Allocation[i][j]."""
        need = {}
        for p in self.processes:
            need[p] = {}
            for r in self.allocation[p]:
                need[p][r] = self.max_matrix[p][r] - self.allocation[p][r]
        return need

    def is_safe(self):
        """Checks if the system is in a safe state using the Banker's Algorithm.

        Returns:
            tuple: (bool, str) where bool indicates if a safe state exists, and str is the safe sequence or error message.
        """
        work = self.available.copy()
        finish = {p: False for p in self.processes}
        safe_sequence = []

        while len(safe_sequence) < len(self.processes):
            found = False
            for p in self.processes:
                if not finish[p]:
                    can_run = all(self.need[p].get(r, 0) <= work.get(r, 0) for r in self.total_resources)
                    if can_run:
                        safe_sequence.append(p)
                        for r in self.allocation[p]:
                            work[r] = work.get(r, 0) + self.allocation[p][r]
                        finish[p] = True
                        found = True
            if not found:
                return False, "No safe sequence found. System may be in an unsafe state or deadlocked."
        return True, f"Safe sequence: {safe_sequence}"

    def detect_deadlock(self):
        """Detects if the system is deadlocked or unsafe.

        Returns:
            tuple: (bool, str) where bool indicates if a deadlock/unsafe state exists, and str is a message.
        """
        if not self.allocation or not self.max_matrix:
            return False, "Please provide allocation and max data before detecting deadlock."
        safe, message = self.is_safe()
        return not safe, message

    def get_need(self):
        """Returns the computed Need matrix."""
        return self.need