setup:
	@poetry install

run:
	@poetry run psudaemon

fix:
	@poetry run ruff check psudaemon/*/*.py  --fix
