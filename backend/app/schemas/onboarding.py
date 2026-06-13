from pydantic import BaseModel, Field, field_validator

# Static allowed IDs; used for request validation and options lookup.
ALLOWED_ASSETS = frozenset({"bitcoin", "ethereum", "solana", "xrp"})
ALLOWED_INVESTOR_TYPES = frozenset({"hodler", "day_trader", "nft_collector"})
ALLOWED_CONTENT_TYPES = frozenset({"market_news", "charts", "social", "fun"})


class OptionItem(BaseModel):
    id: str
    label: str


class OnboardingOptionsResponse(BaseModel):
    assets: list[OptionItem]
    investor_types: list[OptionItem]
    content_types: list[OptionItem]


class OnboardingPreferencesResponse(BaseModel):
    assets: list[str]
    investor_type: str | None
    content_types: list[str]
    onboarding_completed: bool


class OnboardingPreferencesUpdate(BaseModel):
    assets: list[str] = Field(..., min_length=1)
    investor_type: str
    content_types: list[str] = Field(..., min_length=1)

    @field_validator("assets")
    @classmethod
    def validate_assets(cls, values: list[str]) -> list[str]:
        deduped = list(dict.fromkeys(values))
        unknown = [value for value in deduped if value not in ALLOWED_ASSETS]
        if unknown:
            raise ValueError(f"Unknown asset(s): {', '.join(unknown)}")
        return deduped

    @field_validator("investor_type")
    @classmethod
    def validate_investor_type(cls, value: str) -> str:
        if value not in ALLOWED_INVESTOR_TYPES:
            raise ValueError(f"Unknown investor type: '{value}'")
        return value

    @field_validator("content_types")
    @classmethod
    def validate_content_types(cls, values: list[str]) -> list[str]:
        deduped = list(dict.fromkeys(values))
        unknown = [value for value in deduped if value not in ALLOWED_CONTENT_TYPES]
        if unknown:
            raise ValueError(f"Unknown content type(s): {', '.join(unknown)}")
        return deduped
