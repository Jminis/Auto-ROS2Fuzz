# fuzzer/gen.py
import os
import glob
from datetime import datetime
from openai import OpenAI

MODEL_NAME = "gpt-4o-mini"
FILE_PATTERNS = ["**/*.cpp", "**/*.h"]
MAX_FILE_LENGTH = 12000

class HarnessGenerator:
    def __init__(self, project_dir: str):
        self.project_dir = project_dir
        self.client = OpenAI()
        self.base_prompt = self._load_prompt_file("fuzzer/baseprompt.txt")
        self.seed_prompt = self._load_prompt_file("fuzzer/seedprompt.txt")

        if not self.base_prompt or not self.seed_prompt:
            raise RuntimeError("[warn] Missing baseprompt.txt or seedprompt.txt")

    def _load_prompt_file(self, file_path: str) -> str:
        if not os.path.exists(file_path):
            return ""
        with open(file_path, "r") as f:
            return f.read()

    def _gather_source_files(self):
        file_paths = []
        for pattern in FILE_PATTERNS:
            file_paths.extend(glob.glob(os.path.join(self.project_dir, pattern), recursive=True))
        return file_paths

    def _build_prompt(self, file_path: str) -> str:
        try:
            with open(file_path, "r") as f:
                content = f.read()
        except Exception as e:
            raise RuntimeError(f"[warn] Could not read {file_path}: {e}")

        if len(content) > MAX_FILE_LENGTH:
            content = content[:MAX_FILE_LENGTH] + "\n// [TRUNCATED DUE TO LENGTH]\n"

        return (
            self.base_prompt.strip() +
            "\n\n" +
            self.seed_prompt.strip() +
            "\n\nBelow is the single project file we are focusing on:\n" +
            f"--- FILE: {file_path}\n{content}\n--- END FILE\n"
        )

    def generate(self):
        source_files = self._gather_source_files()
        if not source_files:
            raise RuntimeError("[warn] No source files found.")

        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        project_name = os.path.basename(self.project_dir.rstrip("/"))
        result_dir = f"build/{project_name}/src/ros2_fuzz/src"
        os.makedirs(result_dir, exist_ok=True)

        for i, file_path in enumerate(source_files):
            print(f"[*] Generating harness for: {file_path}")
            prompt = self._build_prompt(file_path)
            code = self.client.chat.completions.create(
                model=MODEL_NAME,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.5
            ).choices[0].message.content

            with open(os.path.join(result_dir, f"fuzz_harness_{i}.cpp"), "w") as f:
                f.write(code)

        print(f"[+] Harness generation complete → {result_dir}")
