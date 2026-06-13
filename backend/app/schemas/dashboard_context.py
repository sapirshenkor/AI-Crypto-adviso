from dataclasses import dataclass


@dataclass(frozen=True)
class DashboardContext:
    """Reusable preference context passed to all dashboard providers."""

    assets: list[str]
    investor_type: str | None
    content_types: list[str]
    onboarding_completed: bool
    use_defaults: bool

    @property
    def wants_market_news(self) -> bool:
        return "market_news" in self.content_types
