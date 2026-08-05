from patchright.async_api import Page
from models import AutomationResult, Status
import tldextract
from abc import ABC, abstractmethod


class SiteAutomator(ABC):
    def __init__(self):
        self.result = AutomationResult(
            domain=None, vote=Status.FAILURE, operation=Status.FAILURE
        )

    async def __call__(self, page: Page, username: str):
        self.result.domain = tldextract.extract(page.url).top_domain_under_public_suffix
        self.result.logs.append(("YELLOW", "STARTING AUTOMATION"))

        self.username = username

        await self.automation(page)
        self.result.logs.append(("YELLOW", "ENDING"))

    @abstractmethod
    async def automation(self, page: Page):
        """Automation fine tuned for specific sites, thus each class inheriting this class must define this method by themselves."""
        pass
