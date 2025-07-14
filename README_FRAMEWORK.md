# NIMDA Development Framework

This repository contains the development framework for NIMDA projects, split into two complementary components:

## 📋 Framework Structure

### 1. SYSTEM_DEV_TEMPLATE.md (Immutable Foundation)
**Purpose:** Universal, unchangeable template for all development projects
**Status:** ⚠️ IMMUTABLE - Cannot be modified
**Sections:** 0-4 (Fundamental rules, validation tools, compliance standards)

**Key Features:**
- Project isolation requirements
- English-only development standards
- Universal validation tools
- Quality assurance guidelines
- Template versioning and migration

### 2. DEV_PLAN.md (Project-Specific Implementation)
**Purpose:** NIMDA v3.2 specific development plan
**Status:** ✅ Extends system template with project details
**Sections:** 1+ (NIMDA-specific architecture, implementation, features)

**Key Features:**
- macOS-optimized implementation
- PySide6 GUI architecture
- AI/ML intelligence systems
- Voice and chat interfaces
- Development roadmap

## 🚀 Usage Workflow

### Initial Setup
```bash
# 1. Navigate to project
cd ~/Projects/NIMDA_v3.2

# 2. MANDATORY: Run system validation
./system_validation.sh

# 3. If validation passes, proceed with development
# 4. If validation fails, system auto-adapts DEV_PLAN.md
```

### Development Session
```bash
# Always start with system validation
cd ~/Projects/NIMDA_v3.2
source venv/bin/activate
./system_validation.sh

# Your development work here...

# End session with compliance check
./english_compliance.sh  # From system template
git commit -m "English-only commit message"
```

## 🔧 Validation and Compliance

### Automatic Validation
- **system_validation.sh**: Ensures DEV_PLAN compliance with system template
- **english_compliance.sh**: Validates English-only development
- **project_validator.py**: Checks project isolation and structure

### Manual Verification
```bash
# Check project location
pwd  # Should be ~/Projects/NIMDA_v3.2

# Verify virtual environment
echo $VIRTUAL_ENV  # Should point to project venv

# Check Git independence
ls .git  # Should exist in project directory
```

## 📁 File Structure

```
nimda_agent_plugin/
├── SYSTEM_DEV_TEMPLATE.md    # Immutable system template
├── DEV_PLAN.md              # NIMDA v3.2 specific plan
├── system_validation.sh     # Mandatory validation script
├── README.md               # This file
└── ... (other project files)
```

## ⚡ Key Principles

### 1. System Template Inheritance
- DEV_PLAN.md **extends** SYSTEM_DEV_TEMPLATE.md
- Section 0-4: From system template (immutable)
- Section 1+: Project-specific content (mutable)

### 2. Compliance-First Development
- Always run `./system_validation.sh` before starting work
- English-only development (code, comments, documentation)
- Project isolation in `~/Projects/{PROJECT_NAME}/`
- Independent Git repository and virtual environment

### 3. Quality Assurance
- Pre-commit hooks for language compliance
- Automated adaptation if DEV_PLAN is non-compliant
- Continuous validation throughout development lifecycle

## 🔄 Template Updates

When SYSTEM_DEV_TEMPLATE.md is updated:
1. Version number increases
2. All projects must re-validate against new template
3. Migration scripts provided for compatibility
4. DEV_PLAN.md auto-adapts to new requirements

## 📞 Support

For questions about:
- **System Template:** Check SYSTEM_DEV_TEMPLATE.md documentation
- **NIMDA Specific:** Refer to DEV_PLAN.md sections 1+
- **Validation Issues:** Run `./system_validation.sh` for diagnostic info

---

**Remember:** Always start with `./system_validation.sh` to ensure compliance! 🎯
