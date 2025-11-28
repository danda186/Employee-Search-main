# Org-level dynamic column configuration (only these fields are returned)
# Order is preserved.
ORG_VISIBLE_COLUMNS = {
    1: ["name", "department", "location", "position", "email"],    # Acme
    2: ["name", "position", "location"],                           # Globex
}

# Default columns (if org not configured)
DEFAULT_COLUMNS = ["name", "department", "position"]
