from patchright.async_api import Page
from models import Status
from utils.helper import log_screenshot, readout_start_automation
from site_actions.base import SiteAutomator


class SiteBestMcServersAutomater(SiteAutomator):
    async def automation(self, page: Page):
        readout_start_automation(page)

        username_input = page.get_by_placeholder("Minecraft Username")
        vote_button = page.get_by_role("button", name="Vote!")

        # print("Filling in username")
        self.result.logs.append(("WHITE", "Filling in username"))
        try:
            await username_input.fill(self.username)
            self.result.logs.append(("GREEN", "FILLED"))
        except TimeoutError:
            self.result.logs.append(("RED", "Unable to fill in username"))
            # print(Fore.RED+"Unable to fill in username")
            return

        # print("Clicking the submit button")
        self.result.logs.append(("WHITE", "Clicking the submit button"))
        try:
            await vote_button.click(delay=200)
            self.result.logs.append(("GREEN", "SUBMITED"))
        except TimeoutError:
            self.result.logs.append(("RED", "Unable to click the submit button"))
            # print(Fore.RED+"Unable to click the submit button")
            return

        # print("Waiting for the page to finish loading, Just in case")
        self.result.logs.append(
            ("WHITE", "Waiting for the page to finish loading, Just in case")
        )
        try:
            await page.wait_for_load_state()
            self.result.logs.append(("GREEN", "LOADED"))
        except TimeoutError:
            self.result.logs.append(("RED", "Failed to achieve load state"))
            return

        # timeout == 20sec
        for i in range(0, 40):
            if page.url == "https://best-minecraft-servers.co/landing":
                # print(Fore.CYAN+"Site is processing the vote")
                self.result.logs.append(("CYAN", "Site is processing the vote"))
                try:
                    await page.wait_for_url("https://best-minecraft-servers.co/")
                    # print(Fore.GREEN+"VOTED")
                    self.result.logs.append(("GREEN", "VOTED"))
                    self.result.vote = Status.SUCCESS
                    self.result.operation = Status.SUCCESS
                    return
                except TimeoutError:
                    self.result.logs.append(("RED", "Vote not registered"))
                    # print(Fore.RED+"Couldnt register vote it seems.")
                    return

            if (
                page.url
                == "https://best-minecraft-servers.co/server-pikanetwork-bestq-pika-host.4401/vote"
                and await page.get_by_text(
                    "You must wait until tomorrow before voting again!"
                ).is_visible()
            ):
                # print(Fore.RED+"Something is wrong, the vote isnt done.")
                # print(Fore.CYAN+"Username already used or Ip already used")
                self.result.logs.append(("CYAN", "Username or Ip already used"))
                self.result.logs.append(("RED", "Vote not registered"))
                self.result.operation = Status.SUCCESS
                return

            await page.wait_for_timeout(500)

        self.result.logs.append(
            ("RED", "Vote not done, and reason is apparently not catched")
        )
        # print(Fore.RED+"Vote not done, and reason is apparently not catched")
        await log_screenshot(page)
