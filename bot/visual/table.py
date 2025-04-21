from rich.table import Table


def generate_table(state_data: dict) -> Table:
    table = Table(title="Bot State Monitor")
    table.add_column("Key", style="cyan", no_wrap=True)
    table.add_column("Value", style="magenta")

    for key, value in state_data.items():
        if key.startswith("_"):
            continue
        table.add_row(str(key), str(value))

    return table
