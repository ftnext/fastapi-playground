fmt:
	@uvx ruff format
	@uvx ruff check --fix --extend-select I

test:
	@uv run pytest --ff -vv

typecheck:
	@uv run mypy .

run:
	@PG_DSN=postgresql+asyncpg://developer:mysecretpassword@127.0.0.1:5432/bookdb uv run uvicorn hello:app --reload
