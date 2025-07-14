# SYSTEM DEVELOPMENT TEMPLATE v1.0

**Template Version:** 1.0  
**Date:** 14.07.2025  
**Purpose:** Universal template for all development projects  
**Status:** IMMUTABLE - This template cannot be modified  

## 0. SYSTEM VALIDATION AND COMPLIANCE

### 0.1. Template Validation Process
**MANDATORY FIRST STEP:** Before any development work begins, validate project compliance:

```bash
#!/bin/bash
# system_validation.sh - REQUIRED first step for all projects
echo "🔍 SYSTEM TEMPLATE VALIDATION STARTING..."

# Step 1: Validate current DEV_PLAN against system template
python3 validate_dev_plan.py

# Step 2: Auto-adapt DEV_PLAN if needed
if [ $? -ne 0 ]; then
    echo "📝 Adapting DEV_PLAN to system template..."
    python3 adapt_dev_plan.py
fi

# Step 3: Verify compliance
python3 final_compliance_check.py

echo "✅ SYSTEM VALIDATION COMPLETE - Ready for development"
```

### 0.2. System Template Validator
```python
# validate_dev_plan.py - Ensures DEV_PLAN follows system template
import os
import sys
from pathlib import Path

class SystemTemplateValidator:
    def __init__(self, dev_plan_path="DEV_PLAN.md"):
        self.dev_plan_path = Path(dev_plan_path)
        self.required_sections = [
            "# PROJECT_NAME Development Plan",
            "## 0. Fundamental Development Rules",
            "### 0.1. Project Isolation and Structure", 
            "### 0.2. Language Requirements",
            "### 0.3. Project Creation Workflow",
            "### 0.4. Compliance Verification"
        ]
        
    def validate_structure(self):
        """Validate DEV_PLAN follows system template structure"""
        if not self.dev_plan_path.exists():
            print("❌ DEV_PLAN.md not found")
            return False
            
        with open(self.dev_plan_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        missing_sections = []
        for section in self.required_sections:
            if section not in content and "PROJECT_NAME" not in section:
                missing_sections.append(section)
                
        if missing_sections:
            print(f"❌ Missing required sections: {missing_sections}")
            return False
            
        print("✅ DEV_PLAN structure validation passed")
        return True
        
    def validate_compliance_rules(self):
        """Validate fundamental rules are present"""
        with open(self.dev_plan_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        required_rules = [
            "~/Projects/{PROJECT_NAME}/",
            "English-only development",
            "Independent Git repository",
            "Isolated virtual environment"
        ]
        
        missing_rules = []
        for rule in required_rules:
            if rule not in content and "{PROJECT_NAME}" not in rule:
                missing_rules.append(rule)
                
        if missing_rules:
            print(f"❌ Missing compliance rules: {missing_rules}")
            return False
            
        print("✅ Compliance rules validation passed")
        return True

if __name__ == "__main__":
    validator = SystemTemplateValidator()
    
    if not validator.validate_structure():
        sys.exit(1)
        
    if not validator.validate_compliance_rules():
        sys.exit(1)
        
    print("🎯 DEV_PLAN fully compliant with system template")
```

## 1. FUNDAMENTAL DEVELOPMENT RULES (IMMUTABLE)

### 1.1. Project Isolation and Structure
**CRITICAL REQUIREMENT:** Every project MUST be completely isolated:

1. **Separate Directory Creation:**
   - Create in: `~/Projects/{PROJECT_NAME}/`
   - NEVER as subdirectory of existing projects
   - Complete independence from other codebases

2. **Independent Lifecycle:**
   - Own Git repository
   - Isolated virtual environment  
   - Separate dependency management
   - Self-contained file structure

3. **Naming Convention:**
   - Pattern: `{PROJECT_NAME}_v{VERSION}`
   - English descriptive names only
   - Clear version identification

### 1.2. Language Requirements (IMMUTABLE)
**MANDATORY:** All development exclusively in English:

1. **Code Elements:**
   - Variable/function/class names in English
   - Comments and docstrings in English
   - Error messages and logs in English

2. **Documentation:**
   - All .md files in English
   - Configuration files in English
   - Git commits in English

3. **File System:**
   - File/directory names in English
   - Python naming conventions (snake_case, PascalCase)

### 1.3. Project Creation Workflow (IMMUTABLE)
**Standard process for all projects:**

```bash
# Universal project creation template
mkdir ~/Projects/{PROJECT_NAME}
cd ~/Projects/{PROJECT_NAME}

git init
echo "# {PROJECT_NAME} - {DESCRIPTION}" > README.md

python3 -m venv venv --upgrade-deps
source venv/bin/activate

mkdir -p {core,modules,services,configs,data,tests}
touch {core,modules,services,tests}/__init__.py

git add .
git commit -m "Initial commit: {PROJECT_NAME} project structure"
```

### 1.4. Compliance Verification (IMMUTABLE)
**Required validation before development:**

- [ ] Project in `~/Projects/{PROJECT_NAME}/`
- [ ] English-only code and documentation
- [ ] Independent Git repository
- [ ] Virtual environment active
- [ ] No external dependencies
- [ ] Naming convention followed

## 2. SYSTEM TOOLS (IMMUTABLE)

### 2.1. English Compliance Checker
```bash
#!/bin/bash
# english_compliance.sh - Universal language validator
echo "🔍 Checking English language compliance..."

# Check for non-ASCII in code files
if grep -r --include="*.py" --include="*.md" --include="*.yaml" --include="*.json" '[^\x00-\x7F]' .; then
    echo "❌ Non-ASCII characters found"
    exit 1
fi

# Check for common non-English patterns
non_english_patterns=(
    "функция" "класс" "переменная" "метод"
    "файл" "папка" "конфиг" "настройка" 
    "пользователь" "система" "ошибка"
)

for pattern in "${non_english_patterns[@]}"; do
    if grep -r --include="*.py" --include="*.md" "$pattern" .; then
        echo "❌ Non-English content: $pattern"
        exit 1
    fi
done

echo "✅ English compliance verified"
```

### 2.2. Project Structure Validator
```python
# project_validator.py - Universal structure checker
import os
import sys
from pathlib import Path

def validate_project_isolation():
    """Ensure project follows isolation rules"""
    current_path = Path.cwd()
    
    # Check location
    if "Projects" not in current_path.parts:
        print("❌ Must be in ~/Projects/ directory")
        return False
        
    # Check Git independence
    if not (current_path / ".git").exists():
        print("❌ Independent Git repository required")
        return False
        
    # Check virtual environment
    if not (current_path / "venv").exists():
        print("❌ Virtual environment required")
        return False
        
    print("✅ Project isolation validated")
    return True

if __name__ == "__main__":
    if not validate_project_isolation():
        sys.exit(1)
```

### 2.3. DEV_PLAN Adapter
```python
# adapt_dev_plan.py - Auto-adapts DEV_PLAN to system template
import re
from pathlib import Path

class DevPlanAdapter:
    def __init__(self, dev_plan_path="DEV_PLAN.md"):
        self.dev_plan_path = Path(dev_plan_path)
        
    def ensure_fundamental_rules(self):
        """Add fundamental rules if missing"""
        with open(self.dev_plan_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        if "## 0. Fundamental Development Rules" not in content:
            # Insert fundamental rules after title
            rules_section = self.get_fundamental_rules_template()
            
            # Find insertion point (after title and metadata)
            lines = content.split('\n')
            insert_index = 0
            
            for i, line in enumerate(lines):
                if line.startswith('**Primary Goal:**'):
                    insert_index = i + 1
                    break
                    
            lines.insert(insert_index, rules_section)
            
            with open(self.dev_plan_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(lines))
                
            print("📝 Added fundamental rules to DEV_PLAN")
            
    def get_fundamental_rules_template(self):
        """Return fundamental rules template"""
        return '''
## 0. Fundamental Development Rules

### 0.1. Project Isolation and Structure
**CRITICAL REQUIREMENT:** This project MUST be completely isolated:

1. **Separate Directory Creation:** `~/Projects/{PROJECT_NAME}/`
2. **Independent Lifecycle:** Own Git, venv, dependencies
3. **No Cross-Dependencies:** All changes within project only

### 0.2. Language Requirements  
**MANDATORY:** English-only development:
- All code/comments in English
- Documentation in English  
- File/directory names in English

### 0.3. Compliance Verification
Before development:
- [ ] Project in isolated directory
- [ ] English-only implementation
- [ ] Independent Git repository
- [ ] Virtual environment active
'''

if __name__ == "__main__":
    adapter = DevPlanAdapter()
    adapter.ensure_fundamental_rules()
    print("✅ DEV_PLAN adapted to system template")
```

## 3. PROJECT LIFECYCLE MANAGEMENT (IMMUTABLE)

### 3.1. Pre-Development Validation
**ALWAYS run before starting any work:**

```bash
# pre_development_check.sh
echo "🚀 Starting pre-development validation..."

# System validation
./system_validation.sh

# Project-specific validation  
python3 project_validator.py

# English compliance
./english_compliance.sh

echo "✅ All validations passed - Development authorized"
```

### 3.2. Development Session Workflow
**Standard process for each coding session:**

1. **Session Start:**
   ```bash
   cd ~/Projects/{PROJECT_NAME}
   source venv/bin/activate
   ./pre_development_check.sh
   ```

2. **Development Work:**
   - Follow English-only rules
   - Maintain project isolation
   - Use proper naming conventions

3. **Session End:**
   ```bash
   ./english_compliance.sh
   git add .
   git commit -m "English-only commit message"
   ```

### 3.3. Quality Gates (IMMUTABLE)
**Required checkpoints:**

- **Daily:** English compliance check
- **Weekly:** Project isolation verification  
- **Before Push:** Full system validation
- **Before Release:** Complete template compliance

## 4. TEMPLATE EXTENSION RULES (IMMUTABLE)

### 4.1. Adding Project-Specific Content
**How to extend this template for specific projects:**

1. **Keep Section 0:** Fundamental rules NEVER change
2. **Add Custom Sections:** Start from Section 1+
3. **Follow Naming:** Use project-specific names
4. **Maintain Compliance:** All additions must follow rules

### 4.2. Template Versioning
**System template version control:**

- Template changes require version bump
- All projects must validate against current template
- Backward compatibility maintained
- Migration scripts provided for template updates

---

**END OF IMMUTABLE SYSTEM TEMPLATE**

*This template provides the foundation for all development projects.*  
*Project-specific DEV_PLANs extend this template with custom content.*  
*The fundamental rules in Section 0-4 cannot be modified.*
