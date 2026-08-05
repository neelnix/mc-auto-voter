from patchright.async_api import Page
from models import Status
from utils.helper import log_screenshot, readout_start_automation
from site_actions.base import SiteAutomator


class SiteMcMpAutomator(SiteAutomator):
    async def automation(self, page: Page):
        readout_start_automation(page)

        username_input = page.locator("#nickname")
        vote_button = page.get_by_role("button", name="Vote")
        policy_checkbox = page.get_by_role(
            "checkbox", name="I agree to Minecraft-mp.com's"
        )

        # print("Filling in username")
        self.result.logs.append(("WHITE", "Filling in username"))
        try:
            await username_input.fill(self.username)
            self.result.logs.append(("GREEN", "FILLED"))
        except TimeoutError:
            self.result.logs.append(("RED", "Unable to fill in username"))
            return

        # print("Clicking the policy checkbox")
        self.result.logs.append(("WHITE", "Clicking the policy checkbox"))
        try:
            await policy_checkbox.check()
            self.result.logs.append(("GREEN", "CHECKED"))
        except TimeoutError:
            self.result.logs.append(("RED", "Unable to check the policy checkbox"))
            return

        # print("Clicking the submit button")
        self.result.logs.append(("WHITE", "Clicking the submit button"))
        try:
            await vote_button.click(delay=200)
            self.result.logs.append(("GREEN", "SUBMITED"))
        except TimeoutError:
            self.result.logs.append(("RED", "Unable to click the submit button"))
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
            if await page.get_by_text("Thank you for your vote!").is_visible():
                self.result.logs.append(("GREEN", "VOTED"))
                self.result.vote = Status.SUCCESS
                self.result.operation = Status.SUCCESS
                # print(Fore.GREEN+"VOTED")
                return

            if await page.get_by_text(
                "You have already voted for this server today"
            ).is_visible():
                self.result.logs.append(("CYAN", "Username or Ip already used"))
                self.result.logs.append(("RED", "Vote not registered"))
                self.result.operation = Status.SUCCESS
                # print(Fore.CYAN+"Username or Ip already used")
                return

            await page.wait_for_timeout(500)

        self.result.logs.append(
            ("RED", "Vote not done, and reason is apparently not catched")
        )
        # print(Fore.RED+"Vote not done, and reason is apparently not catched")
        await log_screenshot(page)
