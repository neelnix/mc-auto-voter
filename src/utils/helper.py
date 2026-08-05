import sys
import tldextract
import time
import os
import requests
import subprocess
from models import AutomationResult, Status
from pathlib import Path
from patchright.async_api import Page
from patchright._impl._driver import compute_driver_executable, get_driver_env
from colorama import Fore


class Timer:
    def __enter__(self):
        self.start = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc, tb):
        self.time = time.perf_counter() - self.start


def get_root_dir() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parents[2]


def get_browsers_path() -> Path:
    return Path(get_root_dir()).joinpath("browsers")


async def log_screenshot(page: Page):
    save_path = Path(get_root_dir()).joinpath(
        "screenshots", tldextract.extract(page.url).domain
    )
    Path(save_path).mkdir(parents=True, exist_ok=True)
    await page.screenshot(
        path=save_path.joinpath(f"screenshot_{time.time()}.jpeg"),
        quality=50,
        full_page=True,
    )


def readout_start_automation(page: Page):
    print(
        f"{Fore.YELLOW}Starting Page Automation For:{Fore.RESET} {tldextract.extract(page.url).top_domain_under_public_suffix}"
    )
    print(f"{Fore.YELLOW}Current page url:{Fore.RESET} {page.url}")


def readout_stats_automation(result: AutomationResult, timer: Timer):
    print(
        f"{Fore.YELLOW}\n{'-' * (15 + len(result.domain))}\nSTATS FOR SITE {result.domain}\n{'-' * (15 + len(result.domain))}\n"
    )
    print(
        f"{Fore.YELLOW}Vote Status: {Fore.RESET}{(Fore.GREEN + 'SUCCESS') if result.vote == Status.SUCCESS else (Fore.RED + 'FAILURE')}"
    )
    print(
        f"{Fore.YELLOW}Operation Status: {Fore.RESET}{(Fore.GREEN + 'SUCCESS') if result.operation == Status.SUCCESS else (Fore.RED + 'FAILURE')}"
    )
    print(f"{Fore.YELLOW}Time Taken: {Fore.RESET}{timer.time:.3f} sec")


def readout_logs_automation(result: AutomationResult):
    print(
        f"{Fore.YELLOW}\n{'-' * (14 + len(result.domain))}\nLOGS FOR SITE {result.domain}\n{'-' * (14 + len(result.domain))}\n"
    )
    for entry in result.logs:
        print(f"{getattr(Fore, entry[0])}{entry[1]}")
    print(f"{Fore.YELLOW}\n{'-' * (14 + len(result.domain))}")


def readout_overall_stats(total_sites, votes_done, operations_done, time_taken):
    print(f"{Fore.YELLOW}\n{'-' * (13)}\nOVERALL STATS\n{'-' * (13)}\n")
    print(
        f"{Fore.YELLOW}Total Votes Done: {Fore.GREEN if votes_done == total_sites else Fore.RED}{votes_done}{Fore.YELLOW}/{total_sites}"
    )
    print(
        f"{Fore.YELLOW}Total Operations Done: {Fore.GREEN if operations_done == total_sites else Fore.RED}{operations_done}{Fore.YELLOW}/{total_sites}"
    )
    print(f"{Fore.YELLOW}Total Time Taken: {time_taken:.3f}")


def readout_retry(cycle_no):
    print(
        f"{Fore.YELLOW}\n{'-' * (18 + len(str(cycle_no)))}\nRETRYING [CYCLE: {cycle_no}]\n{'-' * (18 + len(str(cycle_no)))}\n"
    )


def env_default(env_var, default=None) -> dict[str, str]:
    value = os.getenv(env_var)

    if value is None:
        if default is None:
            raise ValueError(
                f"{Fore.CYAN}NO {env_var} FOUND IN .env, please ensure the .env file is setup properly"
            )
        return {"default": default}

    return {"default": value}


def get_urls(env_var) -> list[str]:
    str_urls = env_default(env_var).get("default")
    return str_urls.replace(" ", "").split(
        ","
    )  # to avoid any error for leading or trailing whitespaces in the urls


def check_for_update(current_version, repo_owner, repo_name):
    if env_default("CHECK_FOR_UPDATE").get("default") != "true":
        return

    print(f"{Fore.CYAN}Current version: {Fore.RESET}{current_version}")

    # fetch latest release from GitHub API
    api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases/latest"
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f"{Fore.RED}Failed to check for updates: {e}")
        return

    latest_version = data.get("tag_name")

    # compare versions
    if latest_version and latest_version != current_version:
        print(f"{Fore.CYAN}Update available: {Fore.RESET}{latest_version}!")
    else:
        print(f"{Fore.GREEN}No updates available")


def check_for_chromium():
    print("Checking for chromium installation")
    driver_executable, driver_cli = compute_driver_executable()
    completed_process = subprocess.run(
        [driver_executable, driver_cli, "install", "chromium"], env=get_driver_env()
    )
    if completed_process.returncode == 0:
        print(f"{Fore.GREEN}CHECKED")


def set_env_browsers_path():
    Path(get_browsers_path()).mkdir(parents=True, exist_ok=True)
    os.environ["PLAYWRIGHT_BROWSERS_PATH"] = str(get_browsers_path())
