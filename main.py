#!/usr/bin/env python3

import os
import sys
from fuzzer.logger import banner, info, warn, error
from fuzzer.gen import HarnessGenerator

def usage():
    info("Usage: python3 main.py <PROJECT_DIR>")
    info("Example: python3 main.py target_projects/turtlebot3\n")

def main():
    banner()

    if len(sys.argv) != 2:
        warn("Missing argument.")
        usage()
        return

    project_path = sys.argv[1]
    if not os.path.isdir(project_path):
        error(f"Invalid path: {project_path}")
        usage()
        return

    try:
        info(f"Loading project: {project_path}")
        generator = HarnessGenerator(project_path)
        generator.generate()

    except Exception as e:
        error(f"Generation failed: {e}")

if __name__ == "__main__":
    main()
