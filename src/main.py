import asyncio
import argparse
import tldextract
from dotenv import load_dotenv
from scrapling.fetchers import AsyncStealthySession
from colorama import Fore, init
from models import Status
from utils.helper import (
    Timer,
    readout_logs_automation,
    readout_stats_automation,
    readout_overall_stats,
    readout_retry,
    get_root_dir,
    env_default,
    check_for_update,
    set_env_browsers_path,
    check_for_chromium,
    get_urls,
)
from site_actions.site_top_mc_servers import SiteTopMcServersAutomator
from site_actions.site_best_mc_servers import SiteBestMcServersAutomater
from site_actions.site_minerank import SiteMinerankAutomator
from site_actions.site_mc_buzz import SiteMcBuzzAutomator
from site_actions.site_mc_krant import SiteMcKrantAutomator
from site_actions.site_mc_mp import SiteMcMpAutomator
from site_actions.site_mc_server_list import SiteMcServerListAutomator


CURRENT_VERSION = "v1.0.0"
REPO_OWNER = "neelnix"
REPO_NAME = "autoVoter"


# site_urls = ['https://minecraftkrant.nl/server/pikanetwork/vote']
# site_urls = ['https://topminecraftservers.org/vote/21765', 'https://best-minecraft-servers.co/server-pikanetwork-bestq-pika-host.4401/vote', 'https://www.minerank.com/pikanetwork/vote', 'https://minecraft.buzz/vote/pikanetwork', 'https://minecraftkrant.nl/server/pikanetwork/vote', 'https://minecraft-mp.com/server/41366/vote/', 'https://minecraft-server-list.com/server/424827/vote/']
# site_urls = ['https://topminecraftservers.org/vote/18687','https://best-minecraft-servers.co/server-jartexnetwork.4402/vote','https://www.minerank.com/jartexnetwork/vote','https://minecraft.buzz/vote/jartexnetwork','https://minecraftkrant.nl/server/jartexnetwork/vote','https://minecraft-mp.com/server/52462/vote/','https://minecraft-server-list.com/server/288369/vote/']
DOMAIN_TO_AUTOMATOR_MAPPING = {
    "topminecraftservers.org": SiteTopMcServersAutomator,
    "best-minecraft-servers.co": SiteBestMcServersAutomater,
    "minerank.com": SiteMinerankAutomator,
    "minecraft.buzz": SiteMcBuzzAutomator,
    "minecraftkrant.nl": SiteMcKrantAutomator,
    "minecraft-mp.com": SiteMcMpAutomator,
    "minecraft-server-list.com": SiteMcServerListAutomator,
}


sites_failed_vote = set()
sites_failed_operation = set()
sites_to_retry = set()


async def fetch(url: str, session: AsyncStealthySession):
    domain = tldextract.extract(url).top_domain_under_public_suffix
    automator = DOMAIN_TO_AUTOMATOR_MAPPING.get(domain)()

    if not automator:
        print(f"{Fore.RED}NO MAPPING FOUND FOR THE URL:{Fore.RESET} {url}")
        return

    with Timer() as timer:
        await session.fetch(
            url, google_search=False, page_action=lambda page: automator(page, USERNAME)
        )

    if automator.result.vote == Status.FAILURE:
        sites_failed_vote.add(url)

    elif automator.result.vote == Status.SUCCESS and (url in sites_failed_vote):
        sites_failed_vote.remove(url)

    if automator.result.operation == Status.FAILURE:
        sites_failed_operation.add(url)

    elif automator.result.operation == Status.SUCCESS and (
        url in sites_failed_operation
    ):
        sites_failed_operation.remove(url)

    readout_stats_automation(automator.result, timer)
    readout_logs_automation(automator.result)


async def main():
    async with AsyncStealthySession(
        headless=HEADLESS,
        solve_cloudflare=True,
        blocked_domains=DOMAINS_TO_BLOCK,
        block_ads=True,
    ) as session:
        with Timer() as main_timer:
            for url in site_urls:
                await fetch(url=url, session=session)

        readout_overall_stats(
            total_sites=len(site_urls),
            votes_done=len(site_urls) - len(sites_failed_vote),
            operations_done=len(site_urls) - len(sites_failed_operation),
            time_taken=main_timer.time,
        )

        if RETRY_COUNT > 0:
            for i in range(0, RETRY_COUNT):
                sites_to_retry = sites_failed_operation.union(sites_failed_vote)

                if not sites_to_retry:
                    break

                readout_retry(cycle_no=i + 1)

                with Timer() as retry_timer:
                    for url in sites_to_retry:
                        await fetch(url=url, session=session)

                readout_overall_stats(
                    total_sites=len(site_urls),
                    votes_done=len(site_urls) - len(sites_failed_vote),
                    operations_done=len(site_urls) - len(sites_failed_operation),
                    time_taken=retry_timer.time,
                )

        # TODO: fix async
        # asyncio doesnt work well for some reason
        # await asyncio.gather(*(session.fetch(url, google_search=False,page_action=globals().get(f"action_option_{key}")) for key,url in site_urls.items()))


if __name__ == "__main__":
    init(autoreset=True, convert=True)
    load_dotenv(dotenv_path=get_root_dir().joinpath(".env"))

    parser = argparse.ArgumentParser(
        description="Auto voter for Pika-Network and Jartex-Network"
    )
    subparser = parser.add_subparsers(
        dest="site", required=True, help="Available Sites"
    )

    parser_pika = subparser.add_parser("pika", help="Auto vote for pika-netword")
    parser_pika.add_argument(
        "-u",
        "--username",
        type=str,
        **env_default("MC_USERNAME"),
        help="Username to use for voting",
    )
    parser_pika.add_argument(
        "-rc",
        "--retry-count",
        type=int,
        **env_default("RETRY_COUNT"),
        help="No of times to retry for failed sites",
    )

    parser_jartex = subparser.add_parser("jartex", help="Auto vote for jartex-network")
    parser_jartex.add_argument(
        "-u",
        "--username",
        type=str,
        **env_default("MC_USERNAME"),
        help="Username to use for voting",
    )
    parser_jartex.add_argument(
        "-rc",
        "--retry-count",
        type=int,
        **env_default("RETRY_COUNT"),
        help="No of times to retry for failed sites",
    )

    args = parser.parse_args()

    check_for_update(CURRENT_VERSION, REPO_OWNER, REPO_NAME)
    set_env_browsers_path()
    check_for_chromium()

    HEADLESS = env_default("RUN_HEADLESS").get("default") == "true"
    DOMAINS_TO_BLOCK = get_urls("DOMAINS_TO_BLOCK")
    USERNAME = args.username
    RETRY_COUNT = args.retry_count
    print(f"{Fore.CYAN}USING USERNAME: {Fore.RESET}{USERNAME}")
    print(f"{Fore.CYAN}RETRY COUNT SET TO: {Fore.RESET}{RETRY_COUNT}")
    print(f"{Fore.CYAN}HEADLESS STATUS SET TO: {Fore.RESET}{HEADLESS}")

    if args.site == "pika":
        site_urls = get_urls("URLS_PIKA")
    elif args.site == "jartex":
        site_urls = get_urls("URLS_JARTEX")

    asyncio.run(main())
    input(f"{Fore.CYAN}\nPress Enter to Exit")
