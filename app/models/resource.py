class Resource:
    def __init__(self, id, cpu_cores, memory_gb):
        self.id = id
        self.total_cpu = cpu_cores
        self.total_memory = memory_gb
        self.available_cpu = cpu_cores
        self.available_memory = memory_gb
        self.tasks = []

    def can_accommodate(self, task):
        return (self.available_cpu >= task.required_cpu and 
                self.available_memory >= task.required_memory)

    def allocate(self, task):
        if self.can_accommodate(task):
            self.available_cpu -= task.required_cpu
            self.available_memory -= task.required_memory
            self.tasks.append(task)
            return True
        return False

    def deallocate(self, task):
        if task in self.tasks:
            self.available_cpu += task.required_cpu
            self.available_memory += task.required_memory
            self.tasks.remove(task) 