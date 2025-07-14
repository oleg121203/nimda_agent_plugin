#!/bin/bash
# create_nimda_project.sh - Example of creating NIMDA v3.2 project following system template

echo "🚀 Creating NIMDA v3.2 project following system template..."

# Step 1: Create project directory (following system template)
echo "📁 Step 1: Creating project directory..."
mkdir -p ~/Projects/NIMDA_v3.2
cd ~/Projects/NIMDA_v3.2

# Step 2: Copy system files
echo "📋 Step 2: Setting up system files..."
cp /Users/dev/Documents/nimda_agent_plugin/SYSTEM_DEV_TEMPLATE.md .
cp /Users/dev/Documents/nimda_agent_plugin/system_validation.sh .
cp /Users/dev/Documents/nimda_agent_plugin/DEV_PLAN.md .
cp /Users/dev/Documents/nimda_agent_plugin/README_FRAMEWORK.md .

# Make validation script executable
chmod +x system_validation.sh

# Step 3: Initialize Git repository
echo "🔧 Step 3: Initializing Git repository..."
git init
echo "# NIMDA v3.2 - Intelligent IT Infrastructure Assistant" > README.md

# Create .gitignore
curl -s -o .gitignore https://raw.githubusercontent.com/github/gitignore/main/Python.gitignore
echo -e "\n# macOS specific\n.DS_Store\n*.app\n*.dmg" >> .gitignore

# Step 4: Create virtual environment
echo "🐍 Step 4: Creating virtual environment..."
python3 -m venv venv --upgrade-deps
source venv/bin/activate

# Step 5: Create project structure
echo "🏗️ Step 5: Creating project structure..."
mkdir -p {core,agents,intelligence,gui,plugins,services,configs,data,tests}
touch {core,agents,intelligence,gui,plugins,services,tests}/__init__.py

# Step 6: Initial commit
echo "💾 Step 6: Initial commit..."
git add .
git commit -m "Initial commit: NIMDA v3.2 project structure"

# Step 7: Run system validation
echo "✅ Step 7: Running system validation..."
./system_validation.sh

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 SUCCESS! NIMDA v3.2 project created and validated"
    echo "📍 Location: ~/Projects/NIMDA_v3.2"
    echo "🔍 Status: Compliant with SYSTEM_DEV_TEMPLATE.md"
    echo ""
    echo "Next steps:"
    echo "1. cd ~/Projects/NIMDA_v3.2"
    echo "2. source venv/bin/activate"
    echo "3. Start development following DEV_PLAN.md"
    echo ""
else
    echo "❌ System validation failed. Check output above."
    exit 1
fi
