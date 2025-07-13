#!/bin/bash
# Git merge strategy for Codex branch priority
# This script should be run when merging Codex branches into main

echo "Applying Codex priority merge strategy..."

# Set merge strategy to prefer incoming changes (Codex branch)
git config merge.ours.driver true
git config merge.tool vimdiff

# For specific Codex branch patterns, use theirs strategy
if [[ "$1" == *"codex"* ]] || [[ "$1" == *"bgrzdn-codex"* ]]; then
    echo "Detected Codex branch: $1"
    echo "Using 'theirs' strategy for merge conflicts"
    
    # Reset any existing merge conflicts with theirs strategy
    git checkout --theirs .
    git add .
    
    echo "Codex branch changes have been prioritized"
else
    echo "Regular merge for branch: $1"
fi
