#!/usr/bin/env python3.11
import subprocess
import sys
import os

# Change to project directory
os.chdir("/Users/dev/Documents/nimda_agent_plugin")

# Run the workflow with python3.11
subprocess.run([sys.executable, "enhanced_interactive_workflow.py"])
