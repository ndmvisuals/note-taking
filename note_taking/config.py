import os
import toml
from pathlib import Path

# Read pyproject.toml
config_file = Path(__file__).resolve().parent / "config.toml"

config = toml.load(config_file)

# Get the BASE_DIR from the configuration
BASE_DIR = Path(config["tool"]["note_taking"]["base_dir"]).resolve()
