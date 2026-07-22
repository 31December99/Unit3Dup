from rich.console import Console


class Menu:
    """
    Create a new Menu.
    VIEW
    """

    def __init__(self):
        self.console = Console()

    def show(self, table) -> None:
        """
        Displays the current page.
        """
        self.console.print(table)
