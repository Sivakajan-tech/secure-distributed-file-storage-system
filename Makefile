# Makefile

.PHONY: format lint

# Command to format code using black
format:
	black -l 79   ./src/Cluster/*.py ./src/MakeChunks/*.py

# Command to run linter
lint:
	flake8 ./src/Cluster/*.py ./src/MakeChunks/*.py
