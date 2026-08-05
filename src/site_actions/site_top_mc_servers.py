from patchright.async_api import Page
from models import Status
from utils.helper import log_screenshot, readout_start_automation
from site_actions.base import SiteAutomator


class SiteTopMcServersAutomator(SiteAutomator):
    async def automation(self, page: Page):
        readout_start_automation(page)

        if "/server/" in page.url:
            # print(Fore.CYAN+"Ip already used for voting today, SKIPPING")
            self.result.logs.append(("CYAN", "Ip already used"))
            self.result.logs.append(("RED", "Vote not registered"))
            self.result.operation = Status.SUCCESS
            return
        elif "/vote/" in page.url:
            # print(Fore.GREEN+"We are at the correct page, VOTING")
            self.result.logs.append(("GREEN", "Correct page loaded"))
        else:
            # print(Fore.RED+"We are not at the correct page it seems, SKIPPING")
            self.result.logs.append(("RED", "Not correct page"))
            self.result.logs.append(("RED", "Vote not registered"))
            await log_screenshot(page)
            return

        username_input = page.locator("#username")
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
            if (
                "/server/" in page.url
                and await page.get_by_text("Thanks for voting!").is_visible()
            ):
                # print(Fore.GREEN+"We voted succesfully")
                self.result.logs.append(("GREEN", "VOTED"))
                self.result.vote = Status.SUCCESS
                self.result.operation = Status.SUCCESS
                return

            if (
                "/vote/" in page.url
                and await page.get_by_text(
                    "Someone has already voted for this server using the username"
                ).is_visible()
            ):
                # print(Fore.RED+"Something is wrong, the vote isnt done.")
                # print(Fore.CYAN+"Username already used")
                self.result.logs.append(("CYAN", "Username already used"))
                self.result.logs.append(("RED", "Vote not registered"))
                self.result.operation = Status.SUCCESS
                return

            await page.wait_for_timeout(500)

        # print("Not an Ip or Username issue")
        self.result.logs.append(
            ("RED", "Vote not done, and reason is apparently not catched")
        )
        await log_screenshot(page)
