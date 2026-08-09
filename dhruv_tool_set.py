from pathlib import Path
import json
import os
import shutil
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
# Terminal colors
# ============================================================

RESET = "\033[0m"

BOLD = "\033[1m"
DIM = "\033[2m"

CYAN = "\033[36m"
BLUE = "\033[34m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
RED = "\033[31m"
WHITE = "\033[37m"


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


def get_terminal_width() -> int:
    return shutil.get_terminal_size((80, 24)).columns


# ============================================================
# Header
# ============================================================

def print_header() -> None:
    width = min(get_terminal_width(), 80)

    title = "D H R U V   T O O L   S E T"
    subtitle = "Terminal Tool Launcher"

    print(f"{CYAN}╔{'═' * (width - 2)}╗{RESET}")

    print(
        f"{CYAN}║{RESET}"
        f"{BOLD}{WHITE}{title:^{width - 2}}{RESET}"
        f"{CYAN}║{RESET}"
    )

    print(
        f"{CYAN}║{RESET}"
        f"{DIM}{subtitle:^{width - 2}}{RESET}"
        f"{CYAN}║{RESET}"
    )

    print(f"{CYAN}╚{'═' * (width - 2)}╝{RESET}")
    print()


# ============================================================
# Input
# ============================================================

def get_choice() -> str:
    return input(f"{GREEN}❯{RESET} ").strip()


# ============================================================
# Menu
# ============================================================

def print_menu_box(title: str, items: list[dict]) -> None:
    width = min(get_terminal_width(), 80)
    inner_width = width - 4

    title_text = f" {title.upper()} "

    if len(title_text) > inner_width:
        title_text = f" {title.upper()[:inner_width - 2]} "

    remaining = inner_width - len(title_text)

    print(
        f"{BLUE}┌─{title_text}"
        f"{'─' * max(0, remaining)}┐{RESET}"
    )

    print(
        f"{BLUE}│{RESET}"
        f"{' ' * (width - 2)}"
        f"{BLUE}│{RESET}"
    )

    for index, item in enumerate(items, start=1):
        number = str(index)
        name = item["name"]

        padding = max(
            0,
            width - 7 - len(number) - len(name)
        )

        print(
            f"{BLUE}│{RESET}"
            f"  {YELLOW}{number:<3}{RESET}"
            f"{WHITE}{name}{RESET}"
            f"{' ' * padding}"
            f"{BLUE}│{RESET}"
        )

    print(
        f"{BLUE}│{RESET}"
        f"{' ' * (width - 2)}"
        f"{BLUE}│{RESET}"
    )

    print(
        f"{BLUE}└{'─' * (width - 2)}┘{RESET}"
    )

    print()


def show_main_menu(categories: list[dict]) -> None:
    clear_screen()
    print_header()

    print_menu_box("Main Menu", categories)

    print(f"  {DIM}exit{RESET}  Exit")
    print()


def show_menu(title: str, items: list[dict]) -> None:
    clear_screen()
    print_header()

    print_menu_box(title, items)

    print(f"  {DIM}0{RESET}     Back")
    print(f"  {DIM}exit{RESET}  Exit")
    print()


# ============================================================
# Runner environment
# ============================================================

def build_runner_environment(
    *configs: dict
) -> dict[str, str]:
    """
    Convert runner configuration from JSON into environment
    variables for the runner.

    Example:

        "app_id": "730"

    becomes:

        DTS_APP_ID=730
    """

    environment = os.environ.copy()

    for config in configs:
        for key, value in config.items():

            # Only pass simple values to runners.
            if isinstance(value, (dict, list)):
                continue

            environment_key = f"DTS_{key.upper()}"

            environment[environment_key] = str(value)

    return environment


# ============================================================
# Runner
# ============================================================

def run_runner(
    runner: str,
    program_name: str,
    *configs: dict
) -> None:

    runner_path = RUNNERS_DIR / runner

    if not runner_path.is_file():
        print()
        print(f"{RED}✗ Runner not found{RESET}")
        print()
        print(f"  {DIM}{runner_path}{RESET}")

        input(
            f"\n{DIM}Press Enter to continue...{RESET}"
        )

        return

    if not os.access(runner_path, os.X_OK):
        print()
        print(f"{RED}✗ Runner is not executable{RESET}")
        print()
        print(f"  {DIM}{runner_path}{RESET}")

        input(
            f"\n{DIM}Press Enter to continue...{RESET}"
        )

        return

    environment = build_runner_environment(*configs)

    result = subprocess.run(
        [str(runner_path)],
        env=environment
    )

    if result.returncode != 0:
        print()
        print(
            f"{RED}✗ Failed to start "
            f"{program_name}{RESET}"
        )

        input(
            f"\n{DIM}Press Enter to continue...{RESET}"
        )


# ============================================================
# Application
# ============================================================

def launch_application(application: dict) -> None:
    versions = application.get("versions", [])

    # --------------------------------------------------------
    # No version list
    # --------------------------------------------------------

    if not versions:
        run_runner(
            application["runner"],
            application["name"],
            application
        )

        return

    # --------------------------------------------------------
    # Single version
    # --------------------------------------------------------

    if len(versions) == 1:
        version = versions[0]

        run_runner(
            version["runner"],
            f"{application['name']} {version['name']}",
            application,
            version
        )

        return

    # --------------------------------------------------------
    # Multiple versions
    # --------------------------------------------------------

    while True:
        show_menu(
            application["name"],
            versions
        )

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
            f"{application['name']} {version['name']}",
            application,
            version
        )

        return


# ============================================================
# Category
# ============================================================

def open_category(category: dict) -> None:
    applications = category.get(
        "applications",
        []
    )

    while True:
        show_menu(
            category["name"],
            applications
        )

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
    categories = config.get(
        "categories",
        []
    )

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

        print(f"{GREEN}✓ Goodbye.{RESET}")
        print(
            f"{DIM}Exiting Dhruv Tool Set...{RESET}"
        )


# ============================================================
# Entry point
# ============================================================

if __name__ == "__main__":
    main()