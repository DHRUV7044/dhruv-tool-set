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
# Application
# ============================================================

APP_NAME = "D H R U V   T O O L   S E T"
APP_SUBTITLE = "Terminal Tool Launcher"
APP_VERSION = "v1.0"

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
# Terminal symbols
# ============================================================

BOX_TOP_LEFT = "╭"
BOX_TOP_RIGHT = "╮"
BOX_BOTTOM_LEFT = "╰"
BOX_BOTTOM_RIGHT = "╯"
BOX_HORIZONTAL = "─"
BOX_VERTICAL = "│"

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
    print("\033[2J\033[H", end="")


def get_terminal_width() -> int:
    return shutil.get_terminal_size((80, 24)).columns


def get_ui_width() -> int:
    return min(max(get_terminal_width(), 60), 100)


# ============================================================
# Header
# ============================================================


def print_header() -> None:
    width = get_ui_width()

    title = APP_NAME
    subtitle = APP_SUBTITLE
    version = APP_VERSION

    print(
        f"{CYAN}{BOX_TOP_LEFT}"
        f"{BOX_HORIZONTAL * (width - 2)}"
        f"{BOX_TOP_RIGHT}{RESET}"
    )

    print(
        f"{CYAN}{BOX_VERTICAL}{RESET}"
        f"{BOLD}{WHITE}{title:^{width - 2}}{RESET}"
        f"{CYAN}{BOX_VERTICAL}{RESET}"
    )

    print(
        f"{CYAN}{BOX_VERTICAL}{RESET}"
        f"{DIM}{subtitle:^{width - 2}}{RESET}"
        f"{CYAN}{BOX_VERTICAL}{RESET}"
    )

    print(
        f"{CYAN}{BOX_VERTICAL}{RESET}"
        f"{DIM}{version:^{width - 2}}{RESET}"
        f"{CYAN}{BOX_VERTICAL}{RESET}"
    )

    print(
        f"{CYAN}{BOX_BOTTOM_LEFT}"
        f"{BOX_HORIZONTAL * (width - 2)}"
        f"{BOX_BOTTOM_RIGHT}{RESET}"
    )

    print()


# ============================================================
# Breadcrumb
# ============================================================


def print_breadcrumb(path: list[str]) -> None:
    if not path:
        return

    parts = [
        f"{DIM}Home{RESET}"
    ]

    for item in path:
        parts.append(
            f"{CYAN}{item}{RESET}"
        )

    breadcrumb = f" {DIM}›{RESET} ".join(parts)

    print(f"  {breadcrumb}")
    print()


# ============================================================
# Input
# ============================================================


def get_choice() -> str:
    return input(
        f"{GREEN}{BOLD}❯{RESET} "
    ).strip()


# ============================================================
# Menu
# ============================================================


def print_menu_box(
    title: str,
    items: list[dict]
) -> None:

    width = get_ui_width()
    inner_width = width - 2

    title_text = f" {title.upper()} "

    if len(title_text) > inner_width - 2:
        title_text = (
            f" {title.upper()[:inner_width - 4]}… "
        )

    remaining = inner_width - len(title_text) - 1

    # --------------------------------------------------------
    # Top
    # --------------------------------------------------------

    print(
        f"{BLUE}{BOX_TOP_LEFT}"
        f"{BOX_HORIZONTAL}{title_text}"
        f"{BOX_HORIZONTAL * max(0, remaining)}"
        f"{BOX_TOP_RIGHT}{RESET}"
    )

    # --------------------------------------------------------
    # Empty line
    # --------------------------------------------------------

    print(
        f"{BLUE}{BOX_VERTICAL}{RESET}"
        f"{' ' * (width - 2)}"
        f"{BLUE}{BOX_VERTICAL}{RESET}"
    )

    # --------------------------------------------------------
    # Items
    # --------------------------------------------------------

    for index, item in enumerate(items, start=1):

        number = str(index)
        name = item["name"]

        number_text = f"{number:>3}"

        available_name_width = width - 11

        if len(name) > available_name_width:
            name = (
                name[:available_name_width - 1]
                + "…"
            )

        padding = max(
            1,
            width
            - 8
            - len(number)
            - len(name)
        )

        print(
            f"{BLUE}{BOX_VERTICAL}{RESET}"
            f"   {YELLOW}{number_text}{RESET}"
            f"  {WHITE}{name}{RESET}"
            f"{' ' * padding}"
            f"{BLUE}{BOX_VERTICAL}{RESET}"
        )

    # --------------------------------------------------------
    # Empty line
    # --------------------------------------------------------

    print(
        f"{BLUE}{BOX_VERTICAL}{RESET}"
        f"{' ' * (width - 2)}"
        f"{BLUE}{BOX_VERTICAL}{RESET}"
    )

    # --------------------------------------------------------
    # Bottom
    # --------------------------------------------------------

    print(
        f"{BLUE}{BOX_BOTTOM_LEFT}"
        f"{BOX_HORIZONTAL * (width - 2)}"
        f"{BOX_BOTTOM_RIGHT}{RESET}"
    )

    print()


# ============================================================
# Main menu
# ============================================================


def show_main_menu(
    categories: list[dict]
) -> None:

    clear_screen()
    print_header()

    print_menu_box(
        "Main Menu",
        categories
    )

    print(
        f"  {DIM}exit{RESET}"
        f"  Exit application"
    )

    print()


# ============================================================
# Standard menu
# ============================================================


def show_menu(
    title: str,
    items: list[dict],
    path: list[str] | None = None
) -> None:

    clear_screen()
    print_header()

    if path:
        print_breadcrumb(path)

    print_menu_box(
        title,
        items
    )

    print(
        f"  {DIM}0{RESET}"
        f"     Back"
    )

    print(
        f"  {DIM}exit{RESET}"
        f"  Exit application"
    )

    print()


# ============================================================
# Runner environment
# ============================================================


def build_runner_environment(
    *configs: dict
) -> dict[str, str]:

    environment = os.environ.copy()

    for config in configs:

        for key, value in config.items():

            # Do not pass nested structures.
            if isinstance(value, (dict, list)):
                continue

            environment_key = (
                f"DTS_{key.upper()}"
            )

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

    # --------------------------------------------------------
    # Runner missing
    # --------------------------------------------------------

    if not runner_path.is_file():

        print()

        print(
            f"{RED}{BOLD}"
            f"✗ Runner not found"
            f"{RESET}"
        )

        print()

        print(
            f"  {DIM}{runner_path}{RESET}"
        )

        input(
            f"\n{DIM}"
            f"Press Enter to continue..."
            f"{RESET}"
        )

        return

    # --------------------------------------------------------
    # Runner not executable
    # --------------------------------------------------------

    if not os.access(
        runner_path,
        os.X_OK
    ):

        print()

        print(
            f"{RED}{BOLD}"
            f"✗ Runner is not executable"
            f"{RESET}"
        )

        print()

        print(
            f"  {DIM}{runner_path}{RESET}"
        )

        input(
            f"\n{DIM}"
            f"Press Enter to continue..."
            f"{RESET}"
        )

        return

    # --------------------------------------------------------
    # Environment
    # --------------------------------------------------------

    environment = build_runner_environment(
        *configs
    )

    # --------------------------------------------------------
    # Execute runner
    # --------------------------------------------------------

    result = subprocess.run(
        [str(runner_path)],
        env=environment
    )

    # --------------------------------------------------------
    # Runner failed
    # --------------------------------------------------------

    if result.returncode != 0:

        print()

        print(
            f"{RED}{BOLD}"
            f"✗ Failed to start "
            f"{program_name}"
            f"{RESET}"
        )

        print(
            f"  {DIM}"
            f"Runner exited with code "
            f"{result.returncode}"
            f"{RESET}"
        )

        input(
            f"\n{DIM}"
            f"Press Enter to continue..."
            f"{RESET}"
        )


# ============================================================
# Application
# ============================================================


def launch_application(
    application: dict,
    path: list[str]
) -> None:

    versions = application.get(
        "versions",
        []
    )

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
            (
                f"{application['name']} "
                f"{version['name']}"
            ),
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
            versions,
            path + [application["name"]]
        )

        choice = get_choice()

        # ----------------------------------------------------
        # Exit
        # ----------------------------------------------------

        if choice.lower() == "exit":
            raise ExitApplication

        # ----------------------------------------------------
        # Back
        # ----------------------------------------------------

        if choice == "0":
            return

        # ----------------------------------------------------
        # Invalid input
        # ----------------------------------------------------

        if not choice.isdigit():
            continue

        index = int(choice)

        if not 1 <= index <= len(versions):
            continue

        # ----------------------------------------------------
        # Launch version
        # ----------------------------------------------------

        version = versions[index - 1]

        run_runner(
            version["runner"],
            (
                f"{application['name']} "
                f"{version['name']}"
            ),
            application,
            version
        )


# ============================================================
# Category
# ============================================================


def open_category(
    category: dict,
    parent_path: list[str]
) -> None:

    applications = category.get(
        "applications",
        []
    )

    while True:

        show_menu(
            category["name"],
            applications,
            parent_path + [category["name"]]
        )

        choice = get_choice()

        # ----------------------------------------------------
        # Exit
        # ----------------------------------------------------

        if choice.lower() == "exit":
            raise ExitApplication

        # ----------------------------------------------------
        # Back
        # ----------------------------------------------------

        if choice == "0":
            return

        # ----------------------------------------------------
        # Invalid input
        # ----------------------------------------------------

        if not choice.isdigit():
            continue

        index = int(choice)

        if not 1 <= index <= len(applications):
            continue

        application = applications[index - 1]

        launch_application(
            application,
            parent_path + [category["name"]]
        )


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

            show_main_menu(
                categories
            )

            choice = get_choice()

            # ------------------------------------------------
            # Exit
            # ------------------------------------------------

            if choice.lower() == "exit":
                raise ExitApplication

            # ------------------------------------------------
            # Invalid input
            # ------------------------------------------------

            if not choice.isdigit():
                continue

            index = int(choice)

            if not 1 <= index <= len(categories):
                continue

            category = categories[index - 1]

            open_category(
                category,
                []
            )

    except ExitApplication:

        clear_screen()
        print_header()

        print(
            f"{GREEN}{BOLD}"
            f"✓ Goodbye."
            f"{RESET}"
        )

        print(
            f"{DIM}"
            f"Exiting Dhruv Tool Set..."
            f"{RESET}"
        )

        print()


# ============================================================
# Entry point
# ============================================================


if __name__ == "__main__":
    main()
