# Description: Times the execution of the solutions to the challenges
# and records the times & results in the README.md file

import time
import os
import importlib.util
from typing import Tuple, Union

def format_results_to_markdown_table(challenge_results) -> str:
    markdown_table = "## Challenges\n\nTable:\n\n"
    markdown_table += "| Day | Task 1 | Task 2 |\n"
    markdown_table += "| --- | ------ | ------ |\n"

    for day, times in sorted(challenge_results.items()):
        markdown_table += f"|  {day} | "
        markdown_table += f"{times['task1_time']:.2f} | "  if times['task1_time'] != None else "   ❌  | "
        markdown_table += f"{times['task2_time']:.2f} | "  if times['task2_time'] != None else "   ❌  | "
        markdown_table += "\n"

    markdown_table += "| --- | ------ | ------ |\n"
    return markdown_table


def run_task(module, task_name) -> Union[bool,float]:
    # Start timing
    start_time = time.time()
    res = False
    # Execute the task
    if hasattr(module, task_name):
        res = getattr(module, task_name)()
    else:
        print(f"Task {task_name} not present for: {module.__name__}")
        return False


    if not res:
        print(f"Task {task_name} failed for: {module.__name__}")
        return False
    

    # End timing
    end_time = time.time()

    return end_time - start_time

def run_challenge(file_path) -> bool | Tuple[float,float]:
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

        day = file.split('.')[0]
        day = day.replace('day', '')
        res = run_challenge(file_path)
        if not res:
            challenge_results[day] = {
                "task1_time": None,
                "task2_time": None
            }
            continue

        res = tuple(res)

        challenge_results[day] = {
            "task1_time": res[0],
            "task2_time": res[1]
        }

    # Write results to README.md
    tbl = format_results_to_markdown_table(challenge_results)

    readme_path = os.path.join(os.path.dirname(__file__), f"README.md")
    with open(readme_path, 'r+') as f:
        readme = f.read()
        readme = readme.split("## Challenges")[0]
        readme += tbl
        f.seek(0)
        f.write(readme)
        f.truncate()


if __name__ == "__main__":
    main()

