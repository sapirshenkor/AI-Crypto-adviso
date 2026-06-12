# External API Integration Skill

When integrating an external API:

1. Create a dedicated backend service.
2. Never call the external API directly from the frontend.
3. Read API keys from environment variables.
4. Add timeout handling.
5. Add error handling.
6. Add fallback static data.
7. Normalize the external API response before returning it to the frontend.
8. Do not leak provider-specific response structures to the frontend.