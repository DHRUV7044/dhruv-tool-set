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
    with CONFIG_FILE.open(
        "r",
        encoding="utf-8"
    ) as file:
        return json.load(file)


# ============================================================
# Terminal
# ============================================================


def clear_screen() -> None:
    print("\033[2J\033[H", end="")


def get_terminal_width() -> int:
    return shutil.get_terminal_size(
        (80, 24)
    ).columns


def get_ui_width() -> int:
    return min(
        max(get_terminal_width(), 60),
        100
    )


# ============================================================
# Header
# ============================================================


def print_header() -> None:
    width = get_ui_width()

    print(
        f"{CYAN}{BOX_TOP_LEFT}"
        f"{BOX_HORIZONTAL * (width - 2)}"
        f"{BOX_TOP_RIGHT}{RESET}"
    )

    print(
        f"{CYAN}{BOX_VERTICAL}{RESET}"
        f"{BOLD}{WHITE}"
        f"{APP_NAME:^{width - 2}}"
        f"{RESET}"
        f"{CYAN}{BOX_VERTICAL}{RESET}"
    )

    print(
        f"{CYAN}{BOX_VERTICAL}{RESET}"
        f"{DIM}"
        f"{APP_SUBTITLE:^{width - 2}}"
        f"{RESET}"
        f"{CYAN}{BOX_VERTICAL}{RESET}"
    )

    print(
        f"{CYAN}{BOX_VERTICAL}{RESET}"
        f"{DIM}"
        f"{APP_VERSION:^{width - 2}}"
        f"{RESET}"
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


def print_breadcrumb(
    path: list[str]
) -> None:

    if not path:
        return

    parts = [
        f"{DIM}Home{RESET}"
    ]

    for index, item in enumerate(path):

        if index == len(path) - 1:
            parts.append(
                f"{BOLD}{WHITE}{item}{RESET}"
            )
        else:
            parts.append(
                f"{DIM}{item}{RESET}"
            )

    breadcrumb = (
        f" {DIM}›{RESET} "
        .join(parts)
    )

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
# Menu item type
# ============================================================


def get_item_indicator(
    item: dict
) -> str:

    if item.get("versions"):
        return f"{CYAN}›{RESET}"

    if item.get("applications"):
        return f"{CYAN}›{RESET}"

    if item.get("groups"):
        return f"{CYAN}›{RESET}"

    return f"{DIM}●{RESET}"


# ============================================================
# Menu box
# ============================================================


def print_menu_box(
    title: str,
    items: list[dict]
) -> None:

    width = get_ui_width()

    title_text = f" {title.upper()} "

    max_title_width = width - 6

    if len(title_text) > max_title_width:
        title_text = (
            f" {title.upper()[:max_title_width - 3]}"
            f"… "
        )

    remaining = (
        width
        - 3
        - len(title_text)
    )

    # --------------------------------------------------------
    # Top border
    # --------------------------------------------------------

    print(
        f"{BLUE}{BOX_TOP_LEFT}"
        f"{BOX_HORIZONTAL}"
        f"{title_text}"
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
    # Menu items
    # --------------------------------------------------------

    for index, item in enumerate(
        items,
        start=1
    ):

        number = str(index)
        name = item["name"]
        indicator = get_item_indicator(item)

        # Leave room for:
        #
        #   │   1   Name                 ●   │
        #

        available_name_width = width - 16

        if len(name) > available_name_width:

            name = (
                name[:available_name_width - 1]
                + "…"
            )

        number_text = (
            f"{YELLOW}{number:>3}{RESET}"
        )

        indicator_text = indicator

        used_width = (
            3
            + 3
            + len(name)
            + 3
            + 1
        )

        padding = max(
            1,
            width - 2 - used_width
        )

        print(
            f"{BLUE}{BOX_VERTICAL}{RESET}"
            f"   "
            f"{number_text}"
            f"   "
            f"{WHITE}{name}{RESET}"
            f"{' ' * padding}"
            f"{indicator_text}"
            f"  "
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
    # Bottom border
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
        f"  Exit"
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
        f"  Exit"
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

            # Nested JSON objects and lists are not passed
            # directly to runner scripts.

            if isinstance(
                value,
                (dict, list)
            ):
                continue

            environment_key = (
                f"DTS_{key.upper()}"
            )

            environment[environment_key] = str(
                value
            )

    return environment


# ============================================================
# Runner
# ============================================================


def run_runner(
    runner: str,
    program_name: str,
    *configs: dict
) -> None:

    runner_path = (
        RUNNERS_DIR / runner
    )

    # --------------------------------------------------------
    # Runner does not exist
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
            f"  {DIM}"
            f"{runner_path}"
            f"{RESET}"
        )

        input(
            f"\n{DIM}"
            f"Press Enter to continue..."
            f"{RESET}"
        )

        return

    # --------------------------------------------------------
    # Runner is not executable
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
            f"  {DIM}"
            f"{runner_path}"
            f"{RESET}"
        )

        input(
            f"\n{DIM}"
            f"Press Enter to continue..."
            f"{RESET}"
        )

        return

    # --------------------------------------------------------
    # Build environment
    # --------------------------------------------------------

    environment = (
        build_runner_environment(
            *configs
        )
    )

    # --------------------------------------------------------
    # Run runner
    # --------------------------------------------------------

    result = subprocess.run(
        [str(runner_path)],
        env=environment
    )

    # --------------------------------------------------------
    # Runner failure
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
    # No versions
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
            path + [
                application["name"]
            ]
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

        # IMPORTANT:
        #
        # Do not return here.
        #
        # After the runner exits, remain in the
        # version-selection menu.


# ============================================================
# Group
# ============================================================


def open_group(
    group: dict,
    parent_path: list[str]
) -> None:

    while True:

        applications = group.get(
            "applications",
            []
        )

        groups = group.get(
            "groups",
            []
        )

        items = applications + groups

        show_menu(
            group["name"],
            items,
            parent_path + [
                group["name"]
            ]
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

        if not 1 <= index <= len(items):
            continue

        item = items[index - 1]

        # ----------------------------------------------------
        # Nested group
        # ----------------------------------------------------

        if item in groups:
            open_group(
                item,
                parent_path + [
                    group["name"]
                ]
            )

        # ----------------------------------------------------
        # Application
        # ----------------------------------------------------

        else:
            launch_application(
                item,
                parent_path + [
                    group["name"]
                ]
            )


# ============================================================
# Category
# ============================================================


def open_category(
    category: dict,
    parent_path: list[str]
) -> None:

    while True:
        applications = category.get(
            "applications",
            []
        )

        groups = category.get(
            "groups",
            []
        )

        items = applications + groups

        show_menu(
            category["name"],
            items,
            parent_path + [
                category["name"]
            ]
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

        if not 1 <= index <= len(items):
            continue

        item = items[index - 1]

        # ----------------------------------------------------
        # Group
        # ----------------------------------------------------

        if item in groups:
            open_group(
                item,
                parent_path + [
                    category["name"]
                ]
            )

        # ----------------------------------------------------
        # Application
        # ----------------------------------------------------

        else:
            launch_application(
                item,
                parent_path + [
                    category["name"]
                ]
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

            category = (
                categories[index - 1]
            )

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
