import toml

try:
    with open("pyproject.toml", "r") as f:
        toml.load(f)
    print("TOML is valid!")
except toml.TomlDecodeError as e:
    print(f"TOML file is invalid: {e}")
