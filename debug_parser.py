#!/usr/bin/env python3
import re


def debug_parser():
    with open("DEV_PLAN_v5.md", "r", encoding="utf-8") as file:
        content = file.read()

    print("=== DEBUGGING PARSER ===")

    # Тестування різних патернів
    patterns = [
        r"## [🎮🧠🚀🌐🔬] Phase (\d+): (.+)",
        r"## .* Phase (\d+): (.+)",
        r"## Phase (\d+):",
        r"Phase (\d+):",
    ]

    for i, pattern in enumerate(patterns):
        print(f"\nPattern {i + 1}: {pattern}")
        matches = re.findall(pattern, content)
        print(f"Matches found: {len(matches)}")
        for match in matches:
            print(f"  {match}")

    # Показати всі рядки з Phase
    print("\n=== ALL LINES WITH 'Phase' ===")
    lines = content.split("\n")
    for i, line in enumerate(lines, 1):
        if "Phase" in line:
            print(f"Line {i}: {line}")


if __name__ == "__main__":
    debug_parser()
