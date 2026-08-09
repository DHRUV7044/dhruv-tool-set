from pathlib import Path
import json
import os
import subprocess


# ============================================================
# Paths
# ============================================================

ROOT = Path(__file__).resolve().parent
CONFIG_FILE = ROOT / "config" / "menu.json"
RUNNERS_DIR = ROOT / "runners"


# ============================================================
# Application exit
# ============================================================

class ExitApplication(Exception):
    pass


# ============================================================
# Configuration
# ============================================================

def load_config() -> dict:
    with CONFIG_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


# ============================================================
# Terminal
# ============================================================

def clear_screen() -> None:
    os.system("clear")


def print_header() -> None:
    print("Welcome to Dhruv Tool Set")
    print("────────────────────────────────")
    print()


# ============================================================
# Input
# ============================================================

def get_choice() -> str:
    return input("Enter: ").strip()


# ============================================================
# Menu
# ============================================================

def show_main_menu(categories: list[dict]) -> None:
    clear_screen()
    print_header()

    print("MAIN MENU")
    print("────────────────────────")

    for index, category in enumerate(categories, start=1):
        print(f"{index}  {category['name']}")

    print()
    print("exit  Exit")


def show_menu(title: str, items: list[dict]) -> None:
    clear_screen()
    print_header()

    print(title.upper())
    print("────────────────────────")

    for index, item in enumerate(items, start=1):
        print(f"{index:02d}  {item['name']}")

    print()
    print("0     Back")
    print("exit  Exit")


# ============================================================
# Runner
# ============================================================

def run_runner(runner: str, program_name: str) -> None:
    runner_path = RUNNERS_DIR / runner

    if not runner_path.is_file():
        print()
        print(f"Runner not found: {runner_path}")
        input("\nPress Enter to continue...")
        return

    if not os.access(runner_path, os.X_OK):
        print()
        print(f"Runner is not executable: {runner_path}")
        input("\nPress Enter to continue...")
        return

    result = subprocess.run([str(runner_path)])

    if result.returncode != 0:
        print()
        print(f"Failed to start {program_name}.")
        input("\nPress Enter to continue...")


# ============================================================
# Application
# ============================================================

def launch_application(application: dict) -> None:
    versions = application.get("versions", [])

    # --------------------------------------------------------
    # Application has no version list
    # --------------------------------------------------------

    if not versions:
        run_runner(
            application["runner"],
            application["name"]
        )
        return

    # --------------------------------------------------------
    # Application has exactly one version
    # --------------------------------------------------------

    if len(versions) == 1:
        version = versions[0]

        run_runner(
            version["runner"],
            f"{application['name']} {version['name']}"
        )
        return

    # --------------------------------------------------------
    # Application has multiple versions
    # --------------------------------------------------------

    while True:
        show_menu(application["name"], versions)

        choice = get_choice()

        if choice.lower() == "exit":
            raise ExitApplication

        if choice == "0":
            return

        if not choice.isdigit():
            continue

        index = int(choice)

        if not 1 <= index <= len(versions):
            continue

        version = versions[index - 1]

        run_runner(
            version["runner"],
            f"{application['name']} {version['name']}"
        )

        return


# ============================================================
# Category
# ============================================================

def open_category(category: dict) -> None:
    applications = category.get("applications", [])

    while True:
        show_menu(category["name"], applications)

        choice = get_choice()

        if choice.lower() == "exit":
            raise ExitApplication

        if choice == "0":
            return

        if not choice.isdigit():
            continue

        index = int(choice)

        if not 1 <= index <= len(applications):
            continue

        application = applications[index - 1]

        launch_application(application)


# ============================================================
# Main
# ============================================================

def main() -> None:
    config = load_config()
    categories = config.get("categories", [])

    try:
        while True:
            show_main_menu(categories)

            choice = get_choice()

            if choice.lower() == "exit":
                raise ExitApplication

            if not choice.isdigit():
                continue

            index = int(choice)

            if not 1 <= index <= len(categories):
                continue

            category = categories[index - 1]

            open_category(category)

    except ExitApplication:
        clear_screen()
        print_header()
        print("Goodbye.")
        print("Exiting Dhruv Tool Set...")


# ============================================================
# Entry point
# ============================================================

if __name__ == "__main__":
    main()
