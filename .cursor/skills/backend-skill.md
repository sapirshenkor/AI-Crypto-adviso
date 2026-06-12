# Backend Skill

Stack:
- FastAPI
- SQLAlchemy
- PostgreSQL
- Alembic
- JWT authentication

Structure:
- app/main.py
- app/core/
- app/db/
- app/models/
- app/schemas/
- app/api/
- app/services/
- app/data/

Rules:
- Routes should be thin.
- Use Pydantic schemas.
- Put business logic in services.
- Use dependency injection for DB sessions and auth user.
- Return clear HTTP errors.
- Keep external API logic inside services.