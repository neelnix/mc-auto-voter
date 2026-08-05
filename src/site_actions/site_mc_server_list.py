from patchright.async_api import Page
from models import Status
from utils.helper import log_screenshot, readout_start_automation
from site_actions.base import SiteAutomator


class SiteMcServerListAutomator(SiteAutomator):
    async def automation(self, page: Page):
        readout_start_automation(page)

        username_input = page.get_by_placeholder("Minecraft playername")
        vote_button = page.locator("#voteButton")

        # print("Filling in username")
        self.result.logs.append(("WHITE", "Filling in username"))
        try:
            await username_input.fill(self.username)
            self.result.logs.append(("GREEN", "FILLED"))
        except TimeoutError:
            self.result.logs.append(("RED", "Unable to fill in username"))
            # print(Fore.RED+"Unable to fill in username")
            return

        # print(Fore.GREEN+"FILLED")

        # print("Clicking the submit button")
        self.result.logs.append(("WHITE", "Clicking the submit button"))
        try:
            await vote_button.click(delay=200)
            self.result.logs.append(("GREEN", "SUBMITED"))
        except TimeoutError:
            self.result.logs.append(("RED", "Unable to click the submit button"))
            # print(Fore.RED+"Unable to click the submit button")
            return
        # print(Fore.GREEN+"SUBMITED")

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
            if await page.get_by_text("Thanks, Vote Registered").is_visible():
                self.result.logs.append(("GREEN", "VOTED"))
                self.result.vote = Status.SUCCESS
                self.result.operation = Status.SUCCESS
                # print(Fore.CYAN+"VOTED")
                return

            if await page.get_by_text("IP already voted today!").is_visible():
                self.result.logs.append(("CYAN", "Ip already used"))
                self.result.logs.append(("RED", "Vote not registered"))
                self.result.operation = Status.SUCCESS
                # print(Fore.CYAN+"Ip already used")
                # print(Fore.RED+"Vote not registered")
                return

            if await page.get_by_text("Username already voted today!").is_visible():
                self.result.logs.append(("CYAN", "Username already used"))
                self.result.logs.append(("RED", "Vote not registered"))
                self.result.operation = Status.SUCCESS
                # print(Fore.CYAN+"Username already used")
                # print(Fore.RED+"Vote not registered")
                return

            if await page.get_by_text(
                "The verification expired due to timeout."
            ).is_visible():
                self.result.logs.append(("RED", "Took too much time, captcha failed"))
                self.result.logs.append(("RED", "Vote not registered"))
                self.result.operation = Status.SUCCESS
                # print(Fore.RED+"Took too much time, captcha failed.")
                # print(Fore.RED+"Vote not registered")
                return

            if await page.get_by_text(
                "Sorry, not a valid playername. (none-premium account)"
            ).is_visible():
                self.result.logs.append(
                    ("RED", "This site needs premium account to vote")
                )
                self.result.logs.append(("RED", "Vote not registered"))
                self.result.operation = Status.SUCCESS
                # print(Fore.RED+"This site needs premium account to vote")
                # print(Fore.RED+"Vote not registered")
                return

            await page.wait_for_timeout(500)
        self.result.logs.append(
            ("RED", "Vote not done, and reason is apparently not catched")
        )
        # print(Fore.RED+"Vote not done, and reason is apparently not catched")
        await log_screenshot(page)
