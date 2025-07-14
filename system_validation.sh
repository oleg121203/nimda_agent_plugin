#!/bin/bash
# system_validation.sh - MANDATORY first step for all projects
# This script ensures DEV_PLAN compliance with SYSTEM_DEV_TEMPLATE

echo "🔍 SYSTEM TEMPLATE VALIDATION STARTING..."
echo "📋 Validating DEV_PLAN against system requirements..."

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is required but not installed"
    exit 1
fi

# Check if we're in a project directory
if [[ "$PWD" != *"/Projects/"* ]]; then
    echo "❌ Must be in a ~/Projects/ subdirectory"
    echo "💡 Current location: $PWD"
    echo "💡 Expected pattern: ~/Projects/{PROJECT_NAME}/"
    exit 1
fi

# Step 1: Validate current DEV_PLAN against system template
echo "📝 Step 1: Validating DEV_PLAN structure..."
python3 -c "
import sys
from pathlib import Path

def validate_dev_plan():
    dev_plan = Path('DEV_PLAN.md')
    if not dev_plan.exists():
        print('❌ DEV_PLAN.md not found')
        return False
        
    with open(dev_plan, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for fundamental sections
    required_sections = [
        '## 0. Fundamental Development Rules',
        '### 0.1. Project Isolation',
        '### 0.2. Language Requirements',
        'English-only development'
    ]
    
    missing = []
    for section in required_sections:
        if section not in content:
            missing.append(section)
    
    if missing:
        print(f'❌ Missing required sections: {missing}')
        return False
        
    print('✅ DEV_PLAN structure validation passed')
    return True

if not validate_dev_plan():
    sys.exit(1)
"

# Step 2: Auto-adapt DEV_PLAN if validation failed
if [ $? -ne 0 ]; then
    echo "📝 Step 2: Auto-adapting DEV_PLAN to system template..."
    python3 -c "
import re
from pathlib import Path

def adapt_dev_plan():
    dev_plan = Path('DEV_PLAN.md')
    
    if not dev_plan.exists():
        print('❌ DEV_PLAN.md not found - cannot adapt')
        return False
        
    with open(dev_plan, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if fundamental rules are missing
    if '## 0. Fundamental Development Rules' not in content:
        print('📝 Adding fundamental rules section...')
        
        # Find insertion point after metadata
        lines = content.split('\n')
        insert_index = 0
        
        for i, line in enumerate(lines):
            if line.startswith('**Primary Goal:**'):
                insert_index = i + 1
                break
                
        # Insert fundamental rules template
        rules_template = '''
## 0. Fundamental Development Rules

### 0.1. Project Isolation and Structure
**CRITICAL REQUIREMENT:** This project MUST be completely isolated:
- Create in: \`~/Projects/{PROJECT_NAME}/\`
- Independent Git repository and virtual environment
- No external project dependencies

### 0.2. Language Requirements
**MANDATORY:** English-only development:
- All code, comments, documentation in English
- File and directory names in English
- Configuration and error messages in English

### 0.3. Compliance Verification
Before development:
- [ ] Project in isolated directory
- [ ] English-only implementation  
- [ ] Independent Git repository
- [ ] Virtual environment active
'''
        
        lines.insert(insert_index, rules_template)
        
        with open(dev_plan, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
            
        print('✅ DEV_PLAN adapted to system template')
        return True
    
    print('✅ DEV_PLAN already compliant')
    return True

if not adapt_dev_plan():
    import sys
    sys.exit(1)
"
    
    # Re-validate after adaptation
    echo "🔄 Re-validating after adaptation..."
    python3 -c "
import sys
from pathlib import Path

def validate_dev_plan():
    dev_plan = Path('DEV_PLAN.md')
    with open(dev_plan, 'r', encoding='utf-8') as f:
        content = f.read()
    
    required_sections = [
        '## 0. Fundamental Development Rules',
        'Project Isolation',
        'Language Requirements',
        'English-only'
    ]
    
    for section in required_sections:
        if section not in content:
            print(f'❌ Still missing: {section}')
            return False
            
    print('✅ DEV_PLAN validation passed after adaptation')
    return True

if not validate_dev_plan():
    sys.exit(1)
"
fi

# Step 3: Final compliance check
echo "📝 Step 3: Final compliance verification..."
python3 -c "
import os
import sys
from pathlib import Path

def final_compliance_check():
    current_path = Path.cwd()
    
    # Check project location
    if 'Projects' not in current_path.parts:
        print('❌ Project not in ~/Projects/ directory')
        return False
    
    # Check for Git repository
    if not (current_path / '.git').exists():
        print('❌ Independent Git repository not found')
        return False
    
    # Check for virtual environment
    if not (current_path / 'venv').exists():
        print('❌ Virtual environment not found')
        return False
    
    # Check if virtual environment is activated
    if not os.environ.get('VIRTUAL_ENV'):
        print('⚠️  Virtual environment not activated (recommended)')
        print('💡 Run: source venv/bin/activate')
    
    print('✅ Final compliance check passed')
    return True

if not final_compliance_check():
    sys.exit(1)
"

echo ""
echo "✅ SYSTEM VALIDATION COMPLETE"
echo "🚀 DEV_PLAN is compliant with system template"
echo "🎯 Ready for project-specific development"
echo ""
