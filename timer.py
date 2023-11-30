# Description: Times the execution of the solutions to the challenges
# and records the times & results in the README.md file

import time
import os
import importlib.util

def run_task(module, task_name):
    # Start timing
    start_time = time.time()

    # Execute the task
    if hasattr(module, task_name):
        getattr(module, task_name)()
    else:
        print(f"Task {task_name} not present for: {module.__name__}")
        return -1

    # End timing
    end_time = time.time()

    return end_time - start_time

def run_challenge(file_path):
    module_name = os.path.basename(file_path).split('.')[0]
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    # Run setup function if it exists
    if hasattr(module, 'setup'):
        module.setup()

    # Run tasks and record times
    task1_time = run_task(module, 'task1')
    task2_time = run_task(module, 'task2')

    return task1_time, task2_time

def main():
    solutions_dir = './solutions'
    challenge_files = [f for f in os.listdir(solutions_dir) if f.endswith('.py')]

    challenge_results = {}
    for file in challenge_files:
        file_path = os.path.join(solutions_dir, file)
        task1_time, task2_time = run_challenge(file_path)
        challenge_results[file] = {
            "task1_time": task1_time,
            "task2_time": task2_time
        }


if __name__ == "__main__":
    main()

