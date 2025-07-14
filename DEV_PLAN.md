# Architectural Modernization Plan for NIMDA v3.2 (macOS-optimized)

**Status:** Ready for Execution  
**Last Updated:** 2025-07-14  
**Primary Goal:** To create an intelligent, autonomous assistant with an advanced "live" interface using Python 3.11 and PySide6, optimized for macOS (M1 Max).

---

## 0. Fundamental Rules & Validation (Immutable)

This section is inherited from the system template. **ALWAYS** begin work with validation.

### 0.1. System Compliance Check
- **Mandatory:** Before starting, execute `./system_validation.sh` to ensure compliance with system requirements.
- **Requirement:** All development must be conducted exclusively in English.

---

## 1. Project Initialization and Setup (macOS-optimized)

### Subtasks:
- [ ] Create and activate a Python 3.11 virtual environment.
- [ ] Install dependencies from `requirements_nimda_v3.txt` (PySide6, PyObjC, FAISS, etc.).
- [ ] Create the complete modular directory structure as specified in the architectural diagram.
- [ ] Configure `.gitignore` for macOS, Python, and PySide6.
- [ ] Initialize the Git repository and make the initial commit.

---

## 2. Core System and Orchestration

### 2.1. `Core/main_controller.py`
- [ ] Implement the main `MainController` class.
- [ ] Integrate the logic for starting and stopping all system components.
- [ ] Create a mechanism to manage data flows between the GUI, agents, and services.

### 2.2. `Core/agent_manager.py`
- [ ] Implement the `AgentManager` class.
- [ ] Add methods to initialize, run, and monitor `ChatAgent` and `WorkerAgent`.
- [ ] Create a task queue to pass structured commands from `ChatAgent` to `WorkerAgent`.

### 2.3. `Core/command_engine.py`
- [ ] Implement CLI command processing for integration with existing plugins.
- [ ] Ensure that `WorkerAgent` can call this module to perform technical tasks.

### 2.4. `run_nimda.py`
- [ ] Create a single entry point for the application.
- [ ] Implement the launch of `MainController` and the main GUI window.

---

## 3. Interaction Model: "Live" Interface and Hierarchical Execution

This is the **key section** that defines NIMDA's uniqueness.

### 3.1. Agent #1: `Agents/chat_agent.py` (Conversationalist & Interpreter)
- [ ] **Free-form Dialogue:** Integrate with an LLM (GPT-4 or equivalent) to conduct natural conversation (jokes, abstract topics).
- [ ] **Intent Detection:** Implement analysis of the user's language "between the lines" to determine their true goals.
- [ ] **Task Formulation:** Create logic to convert a user's free-form request into a clear, structured JSON object with tasks for the `WorkerAgent`.
- [ ] **Quality Control Loop:** Implement a mechanism to review the report from `WorkerAgent`. If the result does not meet the quality level from `app_settings.json` (e.g., `high`), the agent must formulate a new, clarifying task for rework **without involving the user**.
- [ ] **Communication:** Provide the final, comprehensive result to the user only after successfully passing the quality control loop.

### 3.2. Agent #2: `Agents/worker_agent.py` (Technical Executor)
- [ ] **Task Reception:** Implement the reception and parsing of JSON objects exclusively from the `AgentManager`.
- [ ] **Workspace Planning:** Based on the task, the agent must decide how to optimally organize the GUI. It should send commands to create and position dynamic child windows (`adaptive_widget.py`) via `GUI/gui_controller.py`.
- [ ] **Technical Task Execution:**
    - Use `Intelligence/adaptive_thinker.py` to build a sequence of CLI commands.
    - Use `Core/command_engine.py` and the plugin system to execute commands.
- [ ] **Analysis and Output:** Analyze execution results and display them in the appropriate adaptive windows, adjusting their size accordingly.
- [ ] **Reporting:** After completing a task, generate a structured execution report and send it back to the `ChatAgent` via the `AgentManager`.

---

## 4. Graphical User Interface (GUI on PySide6)

### 4.1. `GUI/theme.py`
- [ ] Create a "hacker" theme: dark colors, green or blue text, terminal-style fonts.
- [ ] Implement a "digital rain" (Matrix) style background animation.

### 4.2. `GUI/main_window.py`
- [ ] Create the main application window using `theme.py`.
- [ ] Place the main components: main chat window, input field, status panel.

### 4.3. `GUI/adaptive_widget.py`
- [ ] Create a universal class for dynamic child windows.
- [ ] Ensure that `WorkerAgent` can create, position, resize, and close these windows.
- [ ] Each window must support displaying both static text and real-time logs.

### 4.4. `GUI/gui_controller.py`
- [ ] **Key Module:** Create an API for precise GUI manipulation.
- [ ] Implement functions that `WorkerAgent` can call: `create_window(config)`, `resize_window(id, new_size)`, `update_content(id, content)`.

---

## 5. Intellectual Systems and Services

### 5.1. `Intelligence/`
- [ ] **`adaptive_thinker.py`:** Implement "Chain-of-Thought" reasoning to build complex command sequences.
- [ ] **`learning_module.py`:** Create a knowledge base (`knowledge_base.json`) to store successful solutions. Integrate vector search (FAISS) for quick retrieval of relevant cases.

### 5.2. `Services/`
- [ ] **`voice_recognizer.py`:** Integrate native macOS speech recognition capabilities via `pyobjc-framework-Speech`.
- [ ] **`translator.py`:** Provide reversible translation for processing documentation in various languages.
- [ ] **`doc_handler.py`:** Implement parsing and vector indexing of CLI documentation for the `universal_adapter.py`.

---

## 6. Finalization, Testing, and Documentation

### 6.1. Testing
- [ ] Create integration tests that verify the full interaction cycle: from a user's voice command to execution by the `WorkerAgent`.
- [ ] Write unit tests for `adaptive_thinker` and `gui_controller`.

### 6.2. Configuration and Documentation
- [ ] `Configs/app_settings.json`: Add a `"quality_threshold": "high" | "medium" | "low"` parameter to be used by the `ChatAgent`.
- [ ] Update `README.md` with a description of the new architecture and interaction model.

### 6.3. Build and Packaging
- [ ] Configure `setup.py` and scripts to create an `.app` bundle for macOS using PyInstaller.
- [ ] Create a DMG image for distribution.