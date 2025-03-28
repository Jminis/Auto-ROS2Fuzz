# 🤖 Auto-ROS2Fuzz

**Auto-ROS2Fuzz** is an automated fuzzing framework for ROS2-based C++ projects. It leverages AI (OpenAI GPT models) to generate LibFuzzer-compatible fuzz harnesses and continuously fuzzes target code using coverage-guided techniques in a Dockerized environment.


## 📁 Project Structure
```python
AutoROS2Fuzz/
│
├── main.py                       # 진입점 (CLI 인터페이스 및 전체 흐름 제어)
│
├── fuzzer/                       # 🔧 퍼징을 위한 유틸리티 및 실행 스크립트
│   ├── logger.py                 # 로그 출력 유틸리티 (컬러 지원 포함)
│   ├── gen.py                    # GPT 기반 하네스 생성기 (HarnessGenerator 클래스)
│   ├── fuzz.py                   # Docker 기반 퍼징 수행 스크립트
│   ├── baseprompt.txt            # 하네스 생성을 위한 기본 프롬프트
│   └── seedprompt.txt            # 하네스 생성을 위한 시드 프롬프트
│
├── target_projects/              # 🎯 퍼징 대상 ROS2 프로젝트 소스코드
│   ├── turtlebot3/               # 예: turtlebot3 전체 프로젝트 소스
│   └── <other_project>/          # 추가 대상 프로젝트
│
├── build/                        # 🏗️ 하네스 생성 및 빌드 디렉토리
│   ├── turtlebot3/               # 하네스 생성 후 이곳에 복사하여 colcon 빌드
│   │   ├── src/ros2_fuzz/src/
│   │   │   ├── fuzz_xyz.cpp      # 하네스 C++ 파일
│   │   │   └── ...
│   │   └── ...                   # CMakeLists.txt 등
│   └── <other_project>/
│
├── results/                      # 📊 퍼징 실행 결과 저장소
│   ├── turtlebot3/
│   │   ├── fuzz_create_node/
│   │   │   ├── logs/             # 퍼징 로그 파일
│   │   │   └── crashes/          # 크래시 입력값 저장
│   │   └── fuzz_create_publisher/
│   │       ├── ...
│   └── <other_project>/
│
└── README.md                     # 설명서
```


## 🚀 Features

- 🧠 **AI-generated LibFuzzer harnesses** using GPT-4 or GPT-4o-mini.
- 🛠️ Fully **Dockerized** fuzzing environment.
- 📦 **Corpus & crash management** per fuzzer.
- ♻️ **Auto Fuzz mode**: Random fuzzer selection + 2-hour timeout rotation.
- 🧼 **Crash deduplication**: Avoids storing redundant crash logs via ASAN summaries.

## 🧰 Requirements

- Python 3.8+
- Docker
- OpenAI Python SDK (`pip install openai`)
- ROS2 Humble-compatible environment (inside Docker image)

## 🔧 Setup & Usage

### 1. Clone & Install

```bash
git clone https://github.com/yourname/auto-ros2fuzz.git
cd auto-ros2fuzz
pip install -r requirements.txt
```

### 2. Place Your Target Project
Copy your ROS2 C++ project (e.g., turtlebot3) under:

```bash
target_projects/turtlebot3/
```

cont.
