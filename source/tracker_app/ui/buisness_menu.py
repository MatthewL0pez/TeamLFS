from pathlib import Path
import sys

if __package__ in {None, ""}:
    current_file = Path(__file__).resolve()
    source_root = current_file.parents[2]
    project_root = current_file.parents[3]

    for path in (project_root, source_root):
        path_str = str(path)
        if path_str not in sys.path:
            sys.path.insert(0, path_str)

from tracker_app.ui.business_menu import *  # noqa: F401,F403


if __name__ == "__main__":
    main()
