# NIMDA Agent GUI Development Plan

**Status:** Ready for execution
**Last updated:** 2025-07-14
**Main goal:** Develop, integrate and test a complete graphical user interface (GUI) based on PySide6 for the NIMDA Agent system, ensuring reliable operation with agents and eliminating hardcode.

-----

## 0. Fundamental Rules and Validation (unchanged)

This section is inherited from the system template. **ALWAYS** start work with validation.

### 0.1. System Compliance Check

- [ ] **Mandatory:** Before starting, run `./system_validation.sh` to ensure compliance with system requirements. If the script is in the root, call it from there: `./system_validation.sh`.
- [ ] **Requirement:** All development must be conducted exclusively in English.

-----

## 1. Project Initialization and Dynamic Adaptation (GUI focus)

### 1.1. GUI Environment Setup

- [ ] **Ensure PySide6 is installed**: Dynamically check for PySide6 and other necessary GUI dependencies (e.g., PyObjC for macOS integration), and install them if missing. This should be part of the general dependency installation process through `universal_creative_workflow.py`.
- [ ] **Create basic GUI structure**: Ensure the existence of main directories and files for GUI: `GUI/theme.py`, `GUI/main_window.py`, `GUI/adaptive_widget.py`, `GUI/gui_controller.py` inside the main project.

-----

## 2. Development and Integration of Graphical Interface (GUI on PySide6)

This section is **key** for creating the GUI.

### 2.1. `GUI/theme.py`

- [ ] Create or refine "hacker" theme: dark colors, green or blue text, terminal-style fonts.
- [ ] Implement background animation in "digital rain" style (Matrix).

### 2.2. `GUI/main_window.py`

- [ ] Create main application window using `theme.py`.
- [ ] Place main components: main chat window, input field, status panel.

### 2.3. `GUI/adaptive_widget.py`

- [ ] Create universal class for dynamic child windows.
- [ ] Ensure that `WorkerAgent` can create, position, resize and close these windows.
- [ ] Each window should support displaying both static text and real-time logs.

### 2.4. `GUI/gui_controller.py`

- [ ] **Key module:** Create API for precise GUI manipulation.
- [ ] Implement functions that `WorkerAgent` can call: `create_window(config)`, `resize_window(id, new_size)`, `update_content(id, content)`.
- [ ] Ensure that `gui_controller.py` can be called directly from `nimda_app.py` to launch GUI.

-----

## 3. GUI Integration with Main Agents

### 3.1. `ChatAgent` and `WorkerAgent` Connection with GUI

- [ ] Modify `ChatAgent` and `WorkerAgent` to interact with `gui_controller.py`.
- [ ] `ChatAgent` should be able to send messages for display in the main chat window of the GUI.
- [ ] `WorkerAgent` should be able to manage dynamic windows: create them to display technical task execution results, update their content and resize.

### 3.2. Configure `nimda_app.py` for GUI Launch

- [ ] Modify the main entry file (`nimda_app.py`) to initialize `MainController` and launch the main GUI window.
- [ ] Add command line options to run the program with or without GUI.

-----

## 4. GUI Testing and Finalization

### 4.1. GUI Testing

- [ ] **Unit tests for GUI components**: Create tests for `theme.py`, `main_window.py`, `adaptive_widget.py`, `gui_controller.py`.
- [ ] **GUI-agent integration tests**: Develop tests that simulate interaction between `ChatAgent`, `WorkerAgent` and GUI, checking correct information display and window management.
- [ ] **End-to-End tests**: Check complete workflow from user input to result display in GUI, including dynamic windows.

### 4.2. Cleanup and Deployment Preparation

- [ ] Ensure that all temporary files and generated artifacts related to GUI are properly placed in subdirectories (`GUI/cache/`, `GUI/logs/`) or ignored by `.gitignore`, so the project directory remains clean.
- [ ] Create updated `setup.py` for correct application packaging with GUI.

-----

## Implementation Commands Sequence

To execute this new development plan, follow this command sequence:

1. **Initial setup and validation:**
   ```bash
   ./system_validation.sh
   ```

2. **Run universal creative workflow with updated DEV PLAN:**
   ```bash
   python3 run_universal_workflow.py
   ```

3. **Launch application with GUI and testing:**
   ```bash
   python nimda_app.py --mode gui
   ```

4. **Run GUI integration tests:**
   ```bash
   python integration_tests.py
   ```

5. **Check overall system status:**
   ```bash
   python system_status.py
   ```
