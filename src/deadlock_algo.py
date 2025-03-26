# src/deadlock_algo.py
class DeadlockDetector:
    def __init__(self, resources_held, resources_wanted, total_resources):
        self.resources_held = resources_held
        self.resources_wanted = resources_wanted
        self.total_resources = total_resources

    def build_rag(self):
        graph = {}
        for process in self.resources_held:
            graph[process] = []
        for i in range(self.total_resources):
            resource = "R" + str(i + 1)
            graph[resource] = []
        for process, resources in self.resources_held.items():
            for resource in resources:
                if resource in graph:
                    graph[resource].append(process)
        for process, resources in self.resources_wanted.items():
            for resource in resources:
                if resource in graph:
                    graph[process].append(resource)
        return graph

    def detect_cycle(self, graph):
        visited = set()
        recursion_stack = set()

        def dfs(node):
            visited.add(node)
            recursion_stack.add(node)
            for neighbor in graph.get(node, []):
                if neighbor not in visited:
                    if dfs(neighbor):
                        return True
                elif neighbor in recursion_stack:
                    return True
            recursion_stack.remove(node)
            return False

        for node in graph:
            if node.startswith("P") and node not in visited:
                if dfs(node):
                    return True
        return False

    def detect_deadlock(self):
        if not self.resources_held or not self.resources_wanted:
            return False, "Please allocate and request resources before detecting deadlock."
        rag = self.build_rag()
        has_deadlock = self.detect_cycle(rag)
        if has_deadlock:
            return True, "A deadlock has been detected in the system!"
        else:
            return False, "No deadlock detected in the system."