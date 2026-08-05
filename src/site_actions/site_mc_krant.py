from patchright.async_api import Page
from models import Status
from utils.helper import log_screenshot, readout_start_automation
from site_actions.base import SiteAutomator


class SiteMcKrantAutomator(SiteAutomator):
    async def automation(self, page: Page):
        readout_start_automation(page)

        username_input = page.locator("#minecraft_name")
        vote_button = page.get_by_role("button", name="Stem op deze server")

        # print("Filling in username")
        self.result.logs.append(("WHITE", "Filling in username"))
        # username_input.fill(USERNAME[:-1])
        try:
            await username_input.press_sequentially(self.username, delay=142)
            self.result.logs.append(("GREEN", "FILLED"))
        except TimeoutError:
            self.result.logs.append(("RED", "Unable to fill in username"))
            return

        self.result.logs.append(("WHITE", "Clicking the submit button"))
        # print("Clicking the submit button")
        try:
            await vote_button.click(delay=207)
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
            if await page.get_by_text("Verificatie actief").is_visible():
                # print(Fore.CYAN+"Site is processing the vote")
                self.result.logs.append(("CYAN", "Site is processing the vote"))
                try:
                    await page.get_by_text("Bedankt voor je stem!").wait_for(
                        state="visible"
                    )
                    self.result.logs.append(("GREEN", "VOTED"))
                    self.result.vote = Status.SUCCESS
                    self.result.operation = Status.SUCCESS
                    # print(Fore.GREEN+"VOTED")
                    return
                except TimeoutError:
                    self.result.logs.append(("RED", "Vote not registered"))
                    # print(Fore.RED+"Couldnt register vote")
                    return

            if await page.get_by_text("Je hebt vandaag al gestemd").is_visible():
                self.result.logs.append(("CYAN", "Username already used"))
                self.result.logs.append(
                    (
                        "CYAN",
                        "Sometimes the site directly shows the already voted, even if vote is registered for first time today",
                    )
                )
                self.result.logs.append(("RED", "Vote maybe/maybenot registered"))
                self.result.operation = Status.SUCCESS
                # print(Fore.CYAN+"Username or Ip already used")
                return

            await page.wait_for_timeout(500)

        self.result.logs.append(
            ("RED", "Vote not done, and reason is apparently not catched")
        )
        # print(Fore.RED+"Vote not done, and reason is apparently not catched")
        await log_screenshot(page)
