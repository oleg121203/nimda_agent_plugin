import shutil
from pathlib import Path


def organize_project_files():
    """
    Organizes the generated project files into a proper structure.
    - Creates a root 'nimda_src_v2' directory.
    - Moves generated module directories into the root directory.
    - Creates a main GUI entry point.
    """
    project_root = Path(__file__).parent
    new_src_dir = project_root / "nimda_src_v2"

    print("🚀 Starting project file organization...")

    # 1. Create the main source directory
    if not new_src_dir.exists():
        print(f"Creating source directory: {new_src_dir}")
        new_src_dir.mkdir()

    # 2. List of directories to move
    dirs_to_move = [
        "core_system",
        "data_layer",
        "agent_system",
        "workflow_engine",
        "unit_tests",
        "integration_tests",
        "tests",  # This was also created
    ]

    # 3. Move directories
    for dir_name in dirs_to_move:
        source_path = project_root / dir_name
        dest_path = new_src_dir / dir_name
        if source_path.exists() and source_path.is_dir():
            if not dest_path.exists():
                print(f"Moving {source_path} -> {dest_path}")
                shutil.move(str(source_path), str(dest_path))
            else:
                # If the destination is a directory, move the source *into* it.
                # This handles cases where some dirs might already exist.
                print(
                    f"Destination {dest_path} exists. Moving contents of {source_path} into it."
                )
                for item in source_path.iterdir():
                    shutil.move(str(item), str(dest_path))
                source_path.rmdir()

        else:
            print(f"Directory {source_path} not found. Skipping.")

    # 4. Create the main GUI entry point file
    main_gui_file = new_src_dir / "main.py"
    print(f"Creating main GUI entry point: {main_gui_file}")

    gui_content = """
import tkinter as tk
from tkinter import ttk

class NimdaGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("NIMDA Agent v5.0 - Enhanced GUI")
        self.geometry("800x600")
        
        # Basic styling
        self.style = ttk.Style(self)
        self.style.theme_use('clam')

        # Main frame
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Title Label
        title_label = ttk.Label(main_frame, text="NIMDA Agent GUI", font=("Helvetica", 18, "bold"))
        title_label.pack(pady=10)

        # Status Label
        status_label = ttk.Label(main_frame, text="Status: All systems operational.", font=("Helvetica", 10))
        status_label.pack(pady=5)
        
        # Placeholder for future content
        placeholder_label = ttk.Label(main_frame, text="[Core System, Agent System, and other modules loaded...]", font=("Courier", 12, "italic"))
        placeholder_label.pack(pady=20, fill=tk.BOTH, expand=True)

        # Quit Button
        quit_button = ttk.Button(main_frame, text="Shutdown", command=self.destroy)
        quit_button.pack(side=tk.BOTTOM, pady=10)

if __name__ == "__main__":
    app = NimdaGUI()
    app.mainloop()
"""
    if not main_gui_file.exists():
        with open(main_gui_file, "w", encoding="utf-8") as f:
            f.write(gui_content)
    else:
        print(f"Main GUI file {main_gui_file} already exists. Skipping creation.")

    print("✅ Project file organization complete.")


if __name__ == "__main__":
    organize_project_files()
