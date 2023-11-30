# Description: Times the execution of the solutions to the challenges
# and records the times & results in the README.md file

import time
import os
import importlib.util
from typing import Tuple, Union

def run_task(module, task_name) -> Union[bool,float]:
    # Start timing
    start_time = time.time()

    # Execute the task
    if hasattr(module, task_name):
        getattr(module, task_name)()
    else:
        print(f"Task {task_name} not present for: {module.__name__}")
        return False

    # End timing
    end_time = time.time()

    return end_time - start_time

def run_challenge(file_path) -> Union[bool,Tuple[float,float]]:
    module_name = os.path.basename(file_path).split('.')[0]
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    # Run setup function if it exists
    if hasattr(module, 'setup'):
        if not module.setup():
            print(f"Setup failed for: {module.__name__}")
            return False

    # Run tasks and record times
    task1_result = run_task(module, 'task1')
    if not task1_result:
        return False

    task2_result = run_task(module, 'task2')
    if not task2_result:
        return False


    return task1_result, task2_result

def main():
    solutions_dir = './solutions'
    challenge_files = [f for f in os.listdir(solutions_dir) if f.endswith('.py')]

    challenge_results = {}
    for file in challenge_files:
        file_path = os.path.join(solutions_dir, file)
        res = run_challenge(file_path)
        if not res:
            continue
        res = tuple(res)

        challenge_results[file] = {
            "task1_time": res[0],
            "task2_time": res[1]
        }


if __name__ == "__main__":
    main()

