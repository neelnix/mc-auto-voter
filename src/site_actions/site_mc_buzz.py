from patchright.async_api import Page
from models import Status
from utils.helper import log_screenshot, readout_start_automation
from site_actions.base import SiteAutomator


class SiteMcBuzzAutomator(SiteAutomator):
    async def automation(self, page: Page):
        readout_start_automation(page)

        username_input = page.locator("#username-input")
        vote_button = page.get_by_role("button", name="Submit")

        # print("Filling in username")
        self.result.logs.append(("WHITE", "Filling in username"))
        try:
            await username_input.fill(self.username)
            self.result.logs.append(("GREEN", "FILLED"))
        except TimeoutError:
            self.result.logs.append(("RED", "Unable to fill in username"))
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

        try:
            await page.get_by_text("Please wait to submit your vote.").wait_for(
                state="visible"
            )
            self.result.logs.append(("CYAN", "Site is processing the vote"))
            # print(Fore.CYAN+"Site is processing the vote")
        except TimeoutError:
            self.result.logs.append(("RED", "Couldn't start the vote submit timer"))
            # print(Fore.RED+"Couldn't start the vote submit timer")
            return

        # timeout == 50sec
        for i in range(
            0, 100
        ):  # remember to change the i==99 value if the 100 is changed
            if (
                await page.frame_locator("iframe")
                .first.get_by_text("Success!")
                .is_visible()
            ):
                self.result.logs.append(("CYAN", "Captcha solved"))
                # print(Fore.CYAN+"Captcha solved")
                try:
                    # await page.frame_locator("iframe").first.get_by_text("Success!").wait_for(state="visible",timeout=50_000)
                    self.result.logs.append(("WHITE", "Submiting captcha"))
                    await page.locator('button[id="captcha_submit"]').click(delay=270)
                    # print(Fore.CYAN+"Submiting captcha")
                    self.result.logs.append(("GREEN", "SUBMITED"))
                    break

                except TimeoutError:
                    self.result.logs.append(("RED", "Couldn't submit captcha"))
                    # print(Fore.RED+"Couldnt submit captcha")
                    return

            if (
                await page.frame_locator("iframe")
                .first.get_by_role("checkbox", name="Verify you are human")
                .is_visible()
            ):
                self.result.logs.append(("WHITE", "Clicking the verify checkbox"))
                try:
                    await page.wait_for_timeout(
                        1247
                    )  # random delay before checking the checkbox
                    await (
                        page.frame_locator("iframe")
                        .first.get_by_role("checkbox", name="Verify you are human")
                        .check()
                    )
                    self.result.logs.append(("GREEN", "CHECKED"))

                except TimeoutError:
                    self.result.logs.append(
                        ("RED", "Unable to check the verify human checkbox")
                    )
                    return

            if (
                i == 99
            ):  # To make the script return if the captcha isnt solved in any way and timeout is achieved
                self.result.logs.append(("RED", "Problem in captcha solving"))
                return

            await page.wait_for_timeout(500)

        self.result.logs.append(("WHITE", "Redirecting to Main Page"))
        try:
            await page.wait_for_url("https://minecraft.buzz/")
            self.result.logs.append(("GREEN", "REDIRECTED"))
        except TimeoutError:
            self.result.logs.append(("RED", "Couldn't redirect to main page"))
            # print(Fore.RED+"Couldnt redirect into the main page.")
            return

        # print("Successfully redirected to the main page")
        for i in range(0, 40):
            if await page.get_by_text("Thank you for voting!").is_visible():
                # print(Fore.GREEN+"VOTED")
                self.result.logs.append(("GREEN", "VOTED"))
                self.result.vote = Status.SUCCESS
                self.result.operation = Status.SUCCESS
                return

            if await page.get_by_text("You already voted today!").is_visible():
                # print(Fore.CYAN+"Username or Ip already used")
                self.result.logs.append(("CYAN", "Username or Ip already used"))
                self.result.logs.append(("RED", "Vote not registered"))
                self.result.operation = Status.SUCCESS
                return

            if await page.get_by_text("Captcha is not valid!").is_visible():
                # print(Fore.RED+"Problem in captcha solving")
                self.result.logs.append(("RED", "Problem in captcha solving"))
                self.result.logs.append(("RED", "Vote not registered"))
                self.result.operation = Status.SUCCESS
                return

            if await page.get_by_text(
                "Proxy Detected. Voting using a proxy is not allowed."
            ).is_visible():
                self.result.logs.append(
                    ("CYAN", "Voting using proxy(vpn) is disabled in this site")
                )
                self.result.logs.append(("RED", "Vote not registered"))
                self.result.operation = Status.SUCCESS
                return

            await page.wait_for_timeout(500)

        self.result.logs.append(
            ("RED", "Vote not done, and reason is apparently not catched")
        )
        # print(Fore.RED+"Vote not done, and reason is apparently not catched")
        await log_screenshot(page)
