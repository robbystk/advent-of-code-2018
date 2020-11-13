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
        return self.dependencies[step]

    def __repr__(self):
        step_strings = []
        for item in self.dependencies:
            dependency_string = ', '.join(dep for dep in self.dependencies[item])
            step_strings.append(f"{item}: [{dependency_string}]")
        return ', '.join(step_strings)

def extract_dependency(string):
    """returns a Dependency object"""
    dependency = string[5]
    step = string[36]
    return Dependency(step, dependency)

def main():
    dependencies = Dependencies()
    steps = set()
    with open(sys.argv[1]) as f:
        for line in f:
            dependency = extract_dependency(line)
            steps.add(dependency.step)
            steps.add(dependency.dependency)
            dependencies.add_dep(dependency)

    print(dependencies)
    steps = list(steps)
    steps.sort()
    print(steps)

if __name__ == "__main__":
    main()
