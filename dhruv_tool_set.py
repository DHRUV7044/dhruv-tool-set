from pathlib import Path
import json
import os
import shutil
import subprocess
import sys


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
APP_VERSION = "v1.1"


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
MAGENTA = "\033[35m"
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
    """
    Load the menu configuration.

    Raises FileNotFoundError / json.JSONDecodeError on failure;
    callers are responsible for presenting a friendly error.
    """

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
    """
    Read a line of input.

    Ctrl+C / Ctrl+D are treated the same as typing "exit" so the
    application never dumps a raw traceback on interruption.
    """

    try:
        return input(
            f"{GREEN}{BOLD}❯{RESET} "
        ).strip()

    except (KeyboardInterrupt, EOFError):
        print()
        raise ExitApplication


# ============================================================
# Menu item type
# ============================================================


def is_container(item: dict) -> bool:
    """
    A container is anything that opens into another menu:
    a category, a group, or a multi-version application.
    """

    return bool(
        item.get("groups")
        or item.get("applications")
        or (
            item.get("versions")
            and len(item["versions"]) > 1
        )
    )


def get_item_indicator(
    item: dict
) -> str:

    if is_container(item):
        return f"{CYAN}›{RESET}"

    return f"{DIM}●{RESET}"


def get_item_count_label(item: dict) -> str:
    """
    Small dim status label showing how many entries a
    container holds, e.g. "(18)". Empty for launchable items.
    """

    if item.get("groups") or item.get("applications"):
        count = len(item.get("groups", [])) + len(item.get("applications", []))
        return f"{DIM}({count}){RESET}"

    versions = item.get("versions")

    if versions and len(versions) > 1:
        return f"{DIM}({len(versions)}){RESET}"

    return ""


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
    # Empty menu
    # --------------------------------------------------------

    if not items:

        message = "No items here."

        print(
            f"{BLUE}{BOX_VERTICAL}{RESET}"
            f"   {DIM}{message}"
            f"{' ' * max(0, width - 5 - len(message))}"
            f"{RESET}{BLUE}{BOX_VERTICAL}{RESET}"
        )

        print(
            f"{BLUE}{BOX_VERTICAL}{RESET}"
            f"{' ' * (width - 2)}"
            f"{BLUE}{BOX_VERTICAL}{RESET}"
        )

        print(
            f"{BLUE}{BOX_BOTTOM_LEFT}"
            f"{BOX_HORIZONTAL * (width - 2)}"
            f"{BOX_BOTTOM_RIGHT}{RESET}"
        )

        print()

        return

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
        count_label = get_item_count_label(item)

        # Leave room for:
        #
        #   │   1   Name            (18)   ›   │
        #

        reserved = 16 + (len(count_label) + 1 if count_label else 0)
        available_name_width = width - reserved

        if len(name) > available_name_width:

            name = (
                name[:max(1, available_name_width - 1)]
                + "…"
            )

        number_text = (
            f"{YELLOW}{number:>3}{RESET}"
        )

        used_width = (
            3
            + 3
            + len(name)
            + 3
            + (len(count_label) + 1 if count_label else 0)
            + 1
        )

        padding = max(
            1,
            width - 2 - used_width
        )

        count_segment = f"{count_label} " if count_label else ""

        print(
            f"{BLUE}{BOX_VERTICAL}{RESET}"
            f"   "
            f"{number_text}"
            f"   "
            f"{WHITE}{name}{RESET}"
            f"{' ' * padding}"
            f"{count_segment}"
            f"{indicator}"
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
# Footer
# ============================================================


def print_footer(
    show_back: bool,
    show_search_hint: bool,
    show_global_search: bool = False
) -> None:

    if show_back:
        print(
            f"  {DIM}0{RESET}"
            f"     Back"
        )

    if show_global_search:
        print(
            f"  {DIM}s{RESET}"
            f"     Search"
        )

    if show_search_hint:
        print(
            f"  {DIM}text{RESET}"
            f"  Filter this menu"
        )

    print(
        f"  {DIM}exit{RESET}"
        f"  Exit"
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
    print_menu_box("Main Menu", categories)
    print_footer(show_back=False, show_search_hint=len(categories) > 8)


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

    print_menu_box(title, items)
    print_footer(show_back=True, show_search_hint=len(items) > 8)


# ============================================================
# Filtering
# ============================================================


def filter_items(items: list[dict], query: str) -> list[dict]:
    query = query.lower()
    return [item for item in items if query in item["name"].lower()]


def show_no_matches(query: str) -> None:
    print(
        f"\n  {YELLOW}"
        f"No items match \"{query}\"."
        f"{RESET}"
    )
    input(
        f"\n{DIM}Press Enter to continue...{RESET}"
    )


# ============================================================
# Global search
#
# Unlike filter_items() above (which only ever looks at the
# menu currently on screen), this walks the ENTIRE
# configuration tree once and produces a flat, searchable
# index. It is purely a lookup layer: launching a result
# always goes through the existing launch_version() /
# launch_application() / open_container() functions, so there
# is exactly one place that knows how to launch anything.
# ============================================================


def build_search_index(
    categories: list[dict]
) -> list[dict]:
    """
    Recursively flatten the menu tree into search entries.

    Each entry is one of:

      kind="container"    a category or group (opens a menu)
      kind="application"  a version-less application (launches directly)
      kind="version"      one specific version of an application
                           (launches that version directly)

    Every entry carries its own full display path, and the
    "haystacks" it should be matched against — this is the
    only place matching-relevant names are chosen, so adding a
    new field to search against later means touching one spot.
    """

    index: list[dict] = []

    def walk(
        node: dict,
        path: list[str]
    ) -> None:

        current_path = path + [node["name"]]

        # A category or group is itself a search result: it
        # opens into a submenu rather than launching anything.
        if node.get("groups") or node.get("applications"):
            index.append({
                "kind": "container",
                "display_name": node["name"],
                "path": current_path,
                "haystacks": [node["name"]],
                "container": node,
            })

        for group in node.get("groups", []):
            walk(group, current_path)

        for application in node.get("applications", []):

            versions = application.get("versions", [])
            application_path = current_path + [application["name"]]

            if not versions:
                index.append({
                    "kind": "application",
                    "display_name": application["name"],
                    "path": application_path,
                    "haystacks": [application["name"]],
                    "application": application,
                })
                continue

            # Every version — even if there is only one — is
            # indexed individually so it can be matched and
            # launched on its own, per-version.
            for version in versions:
                index.append({
                    "kind": "version",
                    "display_name": (
                        f"{application['name']} "
                        f"{version['name']}"
                    ),
                    "path": application_path + [version["name"]],
                    "haystacks": [
                        application["name"],
                        version["name"],
                    ],
                    "application": application,
                    "version": version,
                })

    for category in categories:
        walk(category, [])

    return index


def search_index(
    index: list[dict],
    query: str
) -> list[dict]:

    query = query.lower()

    return [
        entry
        for entry in index
        if any(
            query in haystack.lower()
            for haystack in entry["haystacks"]
        )
    ]


def format_path(path: list[str]) -> str:
    return f" {DIM}›{RESET} ".join(path)


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


def show_launch_status(program_name: str) -> None:
    print(
        f"\n  {CYAN}▶ Launching {program_name}...{RESET}\n"
    )


def run_runner(
    runner: str | None,
    program_name: str,
    *configs: dict
) -> None:

    # --------------------------------------------------------
    # Missing "runner" key in configuration
    # --------------------------------------------------------

    if not runner:

        print(
            f"\n{RED}{BOLD}✗ No runner configured for "
            f"{program_name}{RESET}"
        )

        input(
            f"\n{DIM}Press Enter to continue...{RESET}"
        )

        return

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

    show_launch_status(program_name)

    try:
        result = subprocess.run(
            [str(runner_path)],
            env=environment
        )
    except OSError as error:

        print(
            f"\n{RED}{BOLD}✗ Failed to start "
            f"{program_name}{RESET}"
        )

        print(
            f"  {DIM}{error}{RESET}"
        )

        input(
            f"\n{DIM}Press Enter to continue...{RESET}"
        )

        return

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


def launch_version(
    application: dict,
    version: dict
) -> None:
    """
    Launch one specific version of an application directly,
    bypassing any version-selection menu.

    This is the single place that knows how to launch a
    version — used by launch_application() for the
    single-version case and the version-menu loop, and reused
    directly by global search so a matched version can be
    launched without duplicating this logic.
    """

    run_runner(
        version.get("runner"),
        (
            f"{application['name']} "
            f"{version['name']}"
        ),
        application,
        version
    )


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
            application.get("runner"),
            application["name"],
            application
        )

        return

    # --------------------------------------------------------
    # Single version
    # --------------------------------------------------------

    if len(versions) == 1:

        launch_version(
            application,
            versions[0]
        )

        return

    # --------------------------------------------------------
    # Multiple versions
    # --------------------------------------------------------

    active_versions = versions
    query = ""

    while True:

        show_menu(
            application["name"] + (f" — \"{query}\"" if query else ""),
            active_versions,
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
            if query:
                # First "0" clears an active filter, second
                # "0" leaves the version menu entirely.
                active_versions = versions
                query = ""
                continue
            return

        # ----------------------------------------------------
        # Numeric selection
        # ----------------------------------------------------

        if choice.isdigit():

            index = int(choice)

            if not 1 <= index <= len(active_versions):
                continue

            version = active_versions[index - 1]

            launch_version(
                application,
                version
            )

            # IMPORTANT:
            #
            # Do not return here.
            #
            # After the runner exits, remain in the
            # version-selection menu.

            continue

        # ----------------------------------------------------
        # Text: filter the version list
        # ----------------------------------------------------

        query = choice
        matches = filter_items(versions, query)

        if not matches:
            show_no_matches(query)
            query = ""
            active_versions = versions
            continue

        active_versions = matches


# ============================================================
# Container (category or group — same shape, handled once)
# ============================================================


def open_container(
    container: dict,
    parent_path: list[str]
) -> None:

    base_applications = container.get("applications", [])
    base_groups = container.get("groups", [])
    base_items = base_applications + base_groups

    active_items = base_items
    query = ""

    while True:

        title = container["name"] + (f" — \"{query}\"" if query else "")

        show_menu(
            title,
            active_items,
            parent_path + [
                container["name"]
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
            if query:
                active_items = base_items
                query = ""
                continue
            return

        # ----------------------------------------------------
        # Numeric selection
        # ----------------------------------------------------

        if choice.isdigit():

            index = int(choice)

            if not 1 <= index <= len(active_items):
                continue

            item = active_items[index - 1]

            # Whether an item is a "group" is determined by
            # identity against the original groups list, not
            # by structural equality, so two groups can never
            # be confused with each other.
            is_group = any(item is group for group in base_groups)

            if is_group:
                open_container(
                    item,
                    parent_path + [
                        container["name"]
                    ]
                )
            else:
                launch_application(
                    item,
                    parent_path + [
                        container["name"]
                    ]
                )

            continue

        # ----------------------------------------------------
        # Text: filter this menu
        # ----------------------------------------------------

        query = choice
        matches = filter_items(base_items, query)

        if not matches:
            show_no_matches(query)
            query = ""
            active_items = base_items
            continue

        active_items = matches


# ============================================================
# Global search UI
# ============================================================


def print_search_results_box(
    matches: list[dict],
    query: str
) -> None:

    width = get_ui_width()

    title_text = f' SEARCH RESULTS FOR "{query}" '
    max_title_width = width - 6

    if len(title_text) > max_title_width:
        title_text = (
            f' SEARCH RESULTS FOR "{query[:max_title_width - 8]}…" '
        )

    remaining = width - 3 - len(title_text)

    print(
        f"{BLUE}{BOX_TOP_LEFT}"
        f"{BOX_HORIZONTAL}"
        f"{title_text}"
        f"{BOX_HORIZONTAL * max(0, remaining)}"
        f"{BOX_TOP_RIGHT}{RESET}"
    )

    print(
        f"{BLUE}{BOX_VERTICAL}{RESET}"
        f"{' ' * (width - 2)}"
        f"{BLUE}{BOX_VERTICAL}{RESET}"
    )

    for index, entry in enumerate(matches, start=1):

        name = entry["display_name"]
        indicator = (
            f"{CYAN}›{RESET}"
            if entry["kind"] == "container"
            else f"{DIM}●{RESET}"
        )

        available_name_width = width - 16

        if len(name) > available_name_width:
            name = (
                name[:max(1, available_name_width - 1)]
                + "…"
            )

        number_text = f"{YELLOW}{index:>3}{RESET}"

        used_width = 3 + 3 + len(name) + 3 + 1
        padding = max(1, width - 2 - used_width)

        print(
            f"{BLUE}{BOX_VERTICAL}{RESET}"
            f"   "
            f"{number_text}"
            f"   "
            f"{WHITE}{name}{RESET}"
            f"{' ' * padding}"
            f"{indicator}"
            f"  "
            f"{BLUE}{BOX_VERTICAL}{RESET}"
        )

        path_text = format_path(entry["path"])
        path_visible_length = len(
            " › ".join(entry["path"])
        )
        available_path_width = width - 10

        if path_visible_length > available_path_width:
            visible = " › ".join(entry["path"])
            visible = (
                visible[:max(1, available_path_width - 1)]
                + "…"
            )
            path_text = f"{DIM}{visible}{RESET}"
            path_visible_length = len(visible)

        path_padding = max(
            0,
            width - 2 - 7 - path_visible_length
        )

        print(
            f"{BLUE}{BOX_VERTICAL}{RESET}"
            f"       "
            f"{DIM}{path_text}{RESET}"
            f"{' ' * path_padding}"
            f"{BLUE}{BOX_VERTICAL}{RESET}"
        )

        print(
            f"{BLUE}{BOX_VERTICAL}{RESET}"
            f"{' ' * (width - 2)}"
            f"{BLUE}{BOX_VERTICAL}{RESET}"
        )

    print(
        f"{BLUE}{BOX_BOTTOM_LEFT}"
        f"{BOX_HORIZONTAL * (width - 2)}"
        f"{BOX_BOTTOM_RIGHT}{RESET}"
    )

    print()


def show_search_results(
    matches: list[dict],
    query: str
) -> None:
    """
    Displays one set of search results and lets the user
    repeatedly launch results from it. Mirrors the
    version-selection menu: launching something does not leave
    this screen, so the user returns here once the runner
    exits.
    """

    while True:

        clear_screen()
        print_header()
        print_breadcrumb(["Search"])
        print_search_results_box(matches, query)
        print_footer(show_back=True, show_search_hint=False)

        choice = get_choice()

        if choice.lower() == "exit":
            raise ExitApplication

        if choice == "0":
            return

        if not choice.isdigit():
            continue

        index = int(choice)

        if not 1 <= index <= len(matches):
            continue

        entry = matches[index - 1]

        if entry["kind"] == "container":
            open_container(
                entry["container"],
                entry["path"][:-1]
            )
        elif entry["kind"] == "version":
            launch_version(
                entry["application"],
                entry["version"]
            )
        else:
            launch_application(
                entry["application"],
                entry["path"][:-1]
            )

        # Stay on the search results after returning from
        # whatever was just opened/launched.


def run_global_search(
    categories: list[dict]
) -> None:
    """
    Entry point for global search, reached from the main menu
    via "s". Builds the index once per search session and lets
    the user run repeated queries from the same prompt.
    """

    index = build_search_index(categories)

    while True:

        clear_screen()
        print_header()
        print_breadcrumb(["Search"])

        print(
            f"  {DIM}Type a query and press Enter. "
            f"0 or empty to go back.{RESET}"
        )
        print()

        query = input(
            f"{GREEN}{BOLD}Search:{RESET} "
        ).strip()

        if query.lower() == "exit":
            raise ExitApplication

        # An empty query (or explicit "0") returns to the main
        # menu rather than matching everything.
        if not query or query == "0":
            return

        matches = search_index(index, query)

        if not matches:

            print(
                f"\n  {YELLOW}"
                f"No results found for \"{query}\"."
                f"{RESET}"
            )

            input(
                f"\n{DIM}Press Enter to continue...{RESET}"
            )

            continue

        show_search_results(matches, query)


# ============================================================
# Main
# ============================================================


def show_config_error(message: str) -> None:
    clear_screen()
    print_header()

    print(
        f"{RED}{BOLD}✗ Could not load configuration{RESET}"
    )
    print()
    print(f"  {DIM}{message}{RESET}")
    print()


def main() -> None:

    try:
        config = load_config()
    except FileNotFoundError:
        show_config_error(f"Config file not found: {CONFIG_FILE}")
        sys.exit(1)
    except json.JSONDecodeError as error:
        show_config_error(f"Invalid JSON in {CONFIG_FILE.name}: {error}")
        sys.exit(1)

    categories = config.get(
        "categories",
        []
    )

    active_categories = categories
    query = ""

    try:

        while True:

            clear_screen()
            print_header()

            title = "Main Menu" + (f" — \"{query}\"" if query else "")
            print_menu_box(title, active_categories)
            print_footer(
                show_back=bool(query),
                show_search_hint=len(categories) > 8,
                show_global_search=True
            )

            choice = get_choice()

            # ------------------------------------------------
            # Exit
            # ------------------------------------------------

            if choice.lower() == "exit":
                raise ExitApplication

            # ------------------------------------------------
            # Global search
            #
            # Reserved at the main menu only — inside a
            # category/group, "s" is just ordinary filter text.
            # ------------------------------------------------

            if choice.lower() == "s":
                run_global_search(categories)
                continue

            # ------------------------------------------------
            # Back (clears an active search)
            # ------------------------------------------------

            if choice == "0":
                active_categories = categories
                query = ""
                continue

            # ------------------------------------------------
            # Numeric selection
            # ------------------------------------------------

            if choice.isdigit():

                index = int(choice)

                if not 1 <= index <= len(active_categories):
                    continue

                category = active_categories[index - 1]

                open_container(
                    category,
                    []
                )

                continue

            # ------------------------------------------------
            # Text: filter the main menu
            # ------------------------------------------------

            query = choice
            matches = filter_items(categories, query)

            if not matches:
                show_no_matches(query)
                query = ""
                active_categories = categories
                continue

            active_categories = matches

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
