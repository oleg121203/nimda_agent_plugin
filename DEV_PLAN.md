# NIMDA v3.2 Development and Modernization Plan

**Version:** 3.2  
**Date:** 14.07.2025  
**System Template:** SYSTEM_DEV_TEMPLATE.md v1.0  
**Tech Stack:** Python 3.11+, PySide6 (Qt for Python), Asyncio  
**Target Platform:** macOS (optimized for Mac Studio M1 Max)  
**Primary Goal:** To create an intelligent, universal, and adaptive assistant for IT infrastructure management, featuring an intuitive voice and text interface that simulates live conversation and provides a dynamic, dialogue-driven workspace.

## 0. System Compliance and Validation

**CRITICAL:** This DEV_PLAN extends SYSTEM_DEV_TEMPLATE.md and MUST be validated before use.

### 0.1. Pre-Development Validation
**MANDATORY FIRST STEP:**
```bash
# Always run system validation before starting work
./system_validation.sh
```

### 0.2. Project-Specific Compliance
This NIMDA v3.2 project follows all fundamental rules from SYSTEM_DEV_TEMPLATE.md:

- ✅ **Project Location:** `~/Projects/NIMDA_v3.2/`
- ✅ **Isolation:** Independent Git repository and virtual environment
- ✅ **Language:** English-only development (code, comments, documentation)
- ✅ **Independence:** No external project dependencies

### 0.3. Template Inheritance
This plan inherits and extends:
- **Section 0-4:** From SYSTEM_DEV_TEMPLATE.md (immutable)
- **Section 1+:** NIMDA v3.2 specific implementation (this document)

## 1. NIMDA v3.2 Specific Implementation

### 1.1. Project Initialization and Setup (macOS-optimized)

#### 1.1.1. Create NIMDA v3.2 Project Directory
```bash
# Following system template requirements
mkdir ~/Projects/NIMDA_v3.2
cd ~/Projects/NIMDA_v3.2

# Run system validation to ensure compliance
./system_validation.sh
```
#### 1.1.2. Initialize Git Repository
```bash
git init
echo "# NIMDA v3.2 - Intelligent IT Infrastructure Assistant" > README.md
# Create .gitignore with Python + macOS patterns
curl -o .gitignore https://raw.githubusercontent.com/github/gitignore/main/Python.gitignore
echo -e "\n# macOS specific\n.DS_Store\n*.app\n*.dmg" >> .gitignore
git add .
git commit -m "Initial commit: NIMDA v3.2 project structure"
```

#### 1.1.3. Setup Virtual Environment (M1 Max optimized)
```bash
# Use Python 3.11+ with Apple Silicon optimization
# Creating isolated environment as per system template
python3 -m venv venv --upgrade-deps
source venv/bin/activate
```

#### 1.1.4. Install Core Dependencies
**requirements.txt** (macOS-specific, English comments only):
```
pyside6>=6.5.0
qasync>=0.24.0
pyobjc-framework-Cocoa>=9.0    # macOS native integration
pyobjc-framework-Speech>=9.0   # macOS Speech framework
pyobjc-framework-AVFoundation>=9.0  # Audio/Video processing
faiss-cpu>=1.7.4               # Vector database CPU optimized for M1
webrtcvad>=2.0.10              # Voice Activity Detection
aiofiles>=23.0.0               # Async file operations
cryptography>=41.0.0           # Security
psutil>=5.9.0                  # System monitoring
```

```bash
pip install -r requirements.txt
```

## 2. NIMDA v3.2 Architecture and Structure

### 2.1. Visual Directory Structure (macOS-optimized)
```
NIMDA_v3/
│
├── .github/
│   └── workflows/
│       └── ci.yml             # GitHub Actions (macOS runners)
│
├── main.py                    # Single entry point with macOS app bundle support
├── app_info.plist            # macOS application metadata
│
├── core/                      # System core and orchestration
│   ├── __init__.py
│   ├── main_controller.py     # Main orchestrator
│   ├── agent_manager.py       # Agent lifecycle management
│   ├── command_engine.py      # CLI command execution
│   └── macos_integration.py   # Native macOS features
│
├── state/                     # Centralized state management
│   ├── __init__.py
│   ├── store.py               # Redux-like state store
│   ├── actions.py             # System actions
│   └── reducers.py            # State modification functions
│
├── agents/                    # Intelligent agents
│   ├── __init__.py
│   ├── chat_agent.py          # Conversational AI
│   └── worker_agent.py        # Technical execution AI
│
├── intelligence/              # AI capabilities
│   ├── __init__.py
│   ├── adaptive_thinker.py    # Chain of Thought reasoning
│   └── learning_module.py     # Experience learning system
│
├── gui/                       # PySide6 GUI (macOS native styling)
│   ├── __init__.py
│   ├── main_window.py         # Main application window
│   ├── chat_panel.py          # Chat interface
│   ├── display_canvas.py      # Dynamic content area
│   ├── output_widgets/        # Custom output widgets
│   │   ├── log_widget.py
│   │   └── table_widget.py
│   ├── gui_controller.py      # GUI manipulation API
│   ├── macos_theme.py         # macOS-native theming
│   └── accessibility.py      # macOS accessibility support
│
├── plugins/                   # Modular CLI system
│   ├── __init__.py
│   ├── base_provider.py       # Abstract provider interface
│   ├── providers/             # CLI plugins
│   │   ├── macos_provider.py  # Native macOS commands
│   │   ├── mikrotik_provider.py
│   │   └── cisco_provider.py
│   └── universal_adapter.py   # Documentation-based adapter
│
├── services/                  # System services
│   ├── __init__.py
│   ├── voice_service.py       # macOS Speech framework integration
│   ├── translator_service.py  # Translation service
│   ├── doc_parser_service.py  # Documentation parsing
│   ├── vectorizer_service.py  # Text vectorization
│   └── macos_services.py      # Native macOS services
│
├── configs/                   # Configuration
│   ├── providers.json         # LLM provider settings
│   ├── app_settings.json      # Application settings
│   └── macos_settings.json    # macOS-specific settings
│
└── data/                      # Runtime data
    ├── knowledge_base/        # Vector database (FAISS)
    ├── cli_docs_cache/        # Documentation cache
    └── logs/                  # Application logs
        └── nimda.log
```

## 3. NIMDA v3.2 Agent Interaction Model

### 3.1. Agent #1: chat_agent.py (Conversationalist & Interpreter)
- **Voice Integration:** Native macOS Speech framework (no external APIs needed)
- **Translation:** Optional RU ↔ EN translation for user input/output only (internal processing always in English)
- **Intent Recognition:** Natural language understanding with GUI command detection (English processing)
- **Task Formalization:** Converts user requests to structured JSON tasks (English field names)
- **Quality Control:** Validates worker agent results before user presentation

### 3.2. Agent #2: worker_agent.py (Technical Executor & UI Orchestrator)
- **Task Processing:** Handles structured JSON tasks from chat_agent (English property names)
- **Workspace Planning:** Designs optimal result presentation on display_canvas
- **Intelligence Integration:** Uses learning_module and adaptive_thinker (English-only reasoning)
- **CLI Execution:** Routes commands through appropriate providers
- **Report Generation:** Compiles technical results for chat_agent (English format)

## 4. NIMDA v3.2 Intelligence Systems

### 4.1. Adaptive Reasoning Engine (adaptive_thinker.py)
Chain of Thought reasoning system for complex problem solving:
```python
# Example reasoning chain for network diagnostics (English-only implementation)
user_goal: "diagnose_network_latency_on_mikrotik"
→ hypothesis_1: "Check router CPU load"
→ query: get_command_for_intent("check_cpu_load") 
→ execute: /system resource print
→ analyze: cpu_load < 10 → hypothesis_rejected
→ hypothesis_2: "Check interface traffic statistics"
→ continue_until: root_cause_found
```

### 4.2. Learning System (learning_module.py)
FAISS-based vector database for experience accumulation:
- **Storage:** Successful case patterns with intent vectors
- **Retrieval:** Semantic similarity search for instant solutions
- **Optimization:** M1 Max CPU-optimized FAISS operations

## 5. NIMDA v3.2 macOS-Specific Implementation

### 5.1. Native macOS Integration
```python
# core/macos_integration.py - English-only implementation
import objc
from Cocoa import NSWorkspace, NSApplication

class MacOSIntegration:
    def setup_dock_icon(self):
        """Configure application dock icon and menu"""
        pass
        
    def setup_global_hotkeys(self):
        """Register system-wide hotkeys using Carbon Events"""
        pass
        
    def setup_notifications(self):
        """Native macOS notification center integration"""
        pass
```

### 5.2. Voice Service (macOS Speech Framework)
```python
# services/voice_service.py - English-only implementation
import objc
from Speech import SFSpeechRecognizer
from AVFoundation import AVSpeechSynthesizer

class MacOSVoiceService:
    def __init__(self):
        self.speech_recognizer = SFSpeechRecognizer.alloc().init()
        self.speech_synthesizer = AVSpeechSynthesizer.alloc().init()
        
    async def speech_to_text(self, audio_data):
        """Native macOS speech recognition"""
        pass
        
    async def text_to_speech(self, text, voice_language="en-US"):
        """Native macOS speech synthesis with English default"""
        pass
```

### 5.3. GUI Theme (macOS Native)
```python
# gui/macos_theme.py - English-only styling definitions
MACOS_DARK_THEME = """
QMainWindow {
    background-color: #1e1e1e;
    color: #ffffff;
}
QWidget {
    background-color: #2d2d2d;
    border: 1px solid #555555;
    border-radius: 8px;
}
/* Native macOS styling with rounded corners and shadows */
/* All UI elements use English text by default */
"""
```

## 6. Testing and Deployment (macOS-focused)

### 6.1. GitHub Actions Workflow (.github/workflows/ci.yml)
```yaml
name: NIMDA macOS CI/CD

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test-macos:
    runs-on: macos-latest
    strategy:
      matrix:
        python-version: ["3.11", "3.12"]
    
    steps:
    - uses: actions/checkout@v4
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies (M1 compatible)
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest pytest-qt flake8
    
    - name: Lint with flake8
      run: |
        flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
        
    - name: Test with pytest
      run: |
        pytest tests/ -v
  
  build-macos-app:
    needs: test-macos
    if: github.ref == 'refs/heads/main'
    runs-on: macos-latest
    
    steps:
    - uses: actions/checkout@v4
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
        
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install pyinstaller
        
    - name: Build macOS App Bundle
      run: |
        pyinstaller main.py \
          --onefile \
          --windowed \
          --name "NIMDA v3" \
          --icon resources/icon.icns \
          --add-data "configs:configs" \
          --add-data "data:data" \
          --osx-bundle-identifier com.nimda.assistant
    
    - name: Create DMG
      run: |
        # Create distributable DMG file
        hdiutil create -volname "NIMDA v3" -srcfolder dist/ -ov -format UDZO nimda_v3_macos.dmg
    
    - name: Upload artifacts
      uses: actions/upload-artifact@v3
      with:
        name: NIMDA-macOS
        path: nimda_v3_macos.dmg
```

## 7. Development Roadmap

### Phase 1: Core & GUI Skeleton (macOS Foundation)
- Complete macOS-optimized project setup
- Implement core architecture with native macOS integration
- Build PySide6 GUI with macOS-native styling
- Integrate qasync for asyncio + Qt event loop

### Phase 2: Basic Communication Flow
- Implement agent communication via Redux store
- Create command_engine with macOS provider
- Integrate native macOS speech services
- Add basic translation capabilities

### Phase 3: Intelligence Layer
- Implement adaptive_thinker with Chain of Thought
- Build learning_module with M1-optimized FAISS
- Add experience accumulation and retrieval

### Phase 4: Universal Adapter & Dynamic GUI
- Develop documentation-based universal_adapter
- Implement dynamic widget management on display_canvas
- Add GUI controller API for agents

### Phase 5: Native Services & Finalization
- Complete macOS Speech framework integration
- Add global hotkey support via PyObjC
- Implement notification center integration
- Optimize for Mac Studio M1 Max performance
- Package as native macOS application (.app bundle)

## 8. macOS-Specific Optimizations

### 8.1. Performance (M1 Max)
- Use M1-optimized NumPy and SciPy builds
- Leverage Metal Performance Shaders for vector operations
- Optimize FAISS for Apple Silicon architecture

### 8.2. User Experience
- Native macOS look and feel
- Spotlight integration for quick launch
- Dock icon with progress indicators
- System preferences integration

### 8.3. Security & Privacy
- Sandbox compatibility
- Microphone access permissions
- Keychain integration for API keys
- Code signing for distribution

## 9. GitHub Actions Workflow Best Practices

### 9.1. YAML Syntax Guidelines for Multi-line Scripts

When working with GitHub Actions, proper formatting of multi-line scripts is crucial:

#### Correct JavaScript usage in actions/github-script:
```yaml
- uses: actions/github-script@v7
  with:
    script: |
      const message = `✅ This branch has been automatically merged into main.
      📋 All conflicts were resolved in favor of the implementation.
      
      The merge strategy ensures that generated changes take precedence.`;
      
      await github.rest.issues.createComment({
        owner: context.repo.owner,
        repo: context.repo.repo,
        issue_number: context.issue.number,
        body: message
      });
```

#### Correct Python code usage in run blocks:
```yaml
- name: Display project info
  run: |
    python -c "
    import os
    print(f'🤖 Project Status: {os.getenv(\"PROJECT_STATUS\", \"active\")}')
    print('📁 Project structure:')
    for root, dirs, files in os.walk('.'):
        level = root.replace('.', '').count(os.sep)
        indent = ' ' * 2 * level
        print(f'{indent}{os.path.basename(root)}/')
        sub_indent = ' ' * 2 * (level + 1)
        for file in files[:5]:
            print(f'{sub_indent}{file}')
        if len(files) > 5:
            print(f'{sub_indent}... and {len(files)-5} more files')
    "
```

### 9.2. YAML File Best Practices

1. **Multi-line strings:** Use `|` to preserve line breaks or `>` to fold lines
2. **Escaping:** In Python strings within YAML, escape quotes as `\"`
3. **Indentation:** YAML is sensitive to indentation - use spaces, not tabs
4. **Code blocks:** JavaScript and Python code must be properly enclosed in a block with `|`

### 9.3. Example GitHub Actions Workflow for NIMDA v3.2

```yaml
name: NIMDA v3.2 CI/CD Pipeline
on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]
  workflow_dispatch:
    inputs:
      environment:
        description: 'Deployment environment'
        required: true
        default: 'development'
        type: choice
        options:
          - development
          - staging
          - production

jobs:
  build-and-test:
    runs-on: macos-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install pytest pytest-cov pytest-qt
      
      - name: Run tests with coverage
        run: |
          pytest tests/ -v --cov=./ --cov-report=xml
      
      - name: Upload coverage reports
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml
          flags: unittests
          name: codecov-umbrella
```

### 9.4. Common YAML Errors and Solutions

| Error | Solution |
|-------|----------|
| Unescaped quotes in Python | Use `\"` instead of `"` |
| JavaScript syntax errors in YAML | Use block `script: \|` |
| Mixed indentation | Use spaces only |
| Invalid YAML syntax | Validate with yamllint or YAML validators |
| Multi-line string issues | Use proper block scalar indicators (`|` or `>`) |

## 10. NIMDA v3.2 Development Workflow

### 10.1. System Template Compliance
**MANDATORY:** This project MUST follow SYSTEM_DEV_TEMPLATE.md requirements:

- **Project Location:** `~/Projects/NIMDA_v3.2/` (isolated directory)
- **Language:** English-only development (all aspects)
- **Independence:** No external project dependencies
- **Validation:** Run `./system_validation.sh` before each development session

### 10.2. NIMDA-Specific Development Process
Following system template compliance, NIMDA v3.2 development includes:

1. **Session Start:**
   ```bash
   cd ~/Projects/NIMDA_v3.2
   source venv/bin/activate
   ./system_validation.sh  # Mandatory system check
   ```

2. **Development Work:**
   - Follow English-only naming conventions
   - Maintain macOS-native integration focus
   - Use PySide6 for GUI components
   - Implement async/await patterns

3. **Session End:**
   ```bash
   # Run English compliance check (from system template)
   python3 -c "
   import subprocess
   result = subprocess.run(['grep', '-r', '--include=*.py', '[^\x00-\x7F]', '.'], 
                          capture_output=True, text=True)
   if result.returncode == 0:
       print('❌ Non-ASCII characters found')
       exit(1)
   print('✅ English compliance verified')
   "
   
   git add .
   git commit -m "English-only commit message describing changes"
   ```

### 10.3. Quality Standards (NIMDA v3.2 Specific)
Building on system template requirements:

- **PEP 8:** Python style with English naming (system requirement)
- **Type Hints:** Full type annotations in English (system requirement)
- **Docstrings:** English documentation for all classes/methods (system requirement)
- **Testing:** >80% coverage with English test names (system requirement)
- **macOS Integration:** Native PyObjC framework usage
- **Performance:** M1 Max optimization for ML/AI components

### 10.4. NIMDA v3.2 Compliance Checklist
Before each commit, verify:

**System Template Compliance:**
- [ ] Project in `~/Projects/NIMDA_v3.2/` directory
- [ ] English-only code, comments, documentation
- [ ] Independent Git repository
- [ ] Virtual environment active
- [ ] No external project dependencies

**NIMDA-Specific Compliance:**
- [ ] macOS-native components use PyObjC
- [ ] PySide6 GUI follows macOS design guidelines
- [ ] Async/await patterns properly implemented
- [ ] Voice services use macOS Speech framework
- [ ] AI components optimized for M1 Max

### 10.5. Integration with System Template
This DEV_PLAN works together with SYSTEM_DEV_TEMPLATE.md:

- **System Template:** Provides immutable foundation (Section 0-4)
- **This Plan:** Adds NIMDA v3.2 specific implementation (Section 1+)
- **Validation:** system_validation.sh ensures compliance
- **Updates:** System template changes require re-validation
