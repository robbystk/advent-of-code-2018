import sys

class Dependency:
    def __init__(self, step, dependency):
        self.step = step
        self.dependency = dependency

    def __str__(self):
        return f"{self.step} depends on {self.dependency}"

    def __repr__(self):
        return f"{self.step} depends on {self.dependency}"

class Dependencies:
    def __init__(self):
        self.dependencies = {}

    def add_dep(self, dependency):
        if dependency.step in self.dependencies:
            self.dependencies[dependency.step].add(dependency.dependency)
        else:
            self.dependencies[dependency.step] = set([dependency.dependency])

    def get_deps(self, step):
        if step in self.dependencies:
            return self.dependencies[step]
        else:
            return set()

    def __repr__(self):
        step_strings = []
        for item in self.dependencies:
            dependency_string = ', '.join(dep for dep in self.dependencies[item])
            step_strings.append(f"{item}: [{dependency_string}]")
        return ', '.join(step_strings)

def is_empty(s):
    """check whether the set is the empty set"""
    return s.issubset({})

def extract_dependency(string):
    """returns a Dependency object"""
    dependency = string[5]
    step = string[36]
    return Dependency(step, dependency)

def get_steps_and_dependencies():
    dependencies = Dependencies()
    steps = set()
    with open(sys.argv[1]) as f:
        for line in f:
            dependency = extract_dependency(line)
            steps.add(dependency.step)
            steps.add(dependency.dependency)
            dependencies.add_dep(dependency)

    return steps, dependencies

def determine_step_sequence(steps, dependencies):
    step_sequence = []
    while not is_empty(steps):
        for step in sorted(steps):
            deps = dependencies.get_deps(step)
            if is_empty(deps - set(step_sequence)):
                step_sequence.append(step)
                steps.remove(step)
                break

    return step_sequence

def seconds_for(step):
    offset = 0
    return ord(step) - 64 + offset

class Worker:
    def __init__(self):
        self.step = None
        self.seconds_left = 0

    def work_on(self, step):
        if self.step is not None:
            raise "Worker is already occupied"
        self.step = step
        self.seconds_left = seconds_for(step)

    def tick(self, coordinator):
        if self.step is not None:
            self.seconds_left -= 1
            if self.seconds_left <= 0:
                coordinator.finish_step(self.step)
                self.step = None

    def is_available(self):
        return self.step is None

    def __repr__(self):
        return f"Working on {self.step} for {self.seconds_left} more seconds"

class Coordinator:
    def __init__(self, workers, steps, dependencies):
        self.workers = workers
        self.steps = steps.copy()
        self.to_do = steps.copy()
        self.dependencies = dependencies
        self.seconds = 0
        self.done = set()

        self.assign_work()

    def finish_step(self, step):
        print(f"Finished step {step}")
        self.done.add(step)

    def assign_available_worker(self, step):
        for worker in self.workers:
            if worker.is_available():
                worker.work_on(step)
                self.to_do.remove(step)
                break

    def assign_work(self):
        for step in sorted(self.to_do):
            deps = self.dependencies.get_deps(step)
            if is_empty(deps - self.done):
                self.assign_available_worker(step)


    def tick(self):
        # advance workers
        for worker in self.workers:
            worker.tick(self)

        self.assign_work()
        self.seconds += 1
        print(self.seconds, self.workers, self.to_do, self.done)

    def run(self):
        while(not self.done >= self.steps):
            self.tick()

def main():
    steps, dependencies = get_steps_and_dependencies()

    print(dependencies)
    print(sorted(steps))

    step_sequence = determine_step_sequence(steps.copy(), dependencies)

    print(''.join(step_sequence))

    N_workers = 2
    workers = [Worker() for _ in range(N_workers)]

    coordinator = Coordinator(workers, steps, dependencies)
    coordinator.run()
    print(coordinator.seconds)

if __name__ == "__main__":
    main()
