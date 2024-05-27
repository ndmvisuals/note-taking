import typer
from rich.console import Console
from rich.table import Table
from note_taking.config import BASE_DIR
from note_taking.file_operations import update_files_and_backlinks
from note_taking.models import RenameResult

console = Console()
app = typer.Typer()

@app.callback()
def callback():
    """
    Note Taking CLI based on PARA
    """

@app.command()
def rename(keyword: str = typer.Argument(...),
           replacement: str = typer.Argument(...),
           force: bool = typer.Option(False, "-f", "--force")):
    """
    Rename files with the given keyword and replacement and update all references to it.
    """
    result = update_files_and_backlinks(keyword, replacement, action=force)

    if not force:
        display_rename_table(result.files_to_rename)
        console.print("[red]Please confirm the changes by running the command again with the[/red] [white]-f[/white] [red]flag")
    else:
        console.print(f"Renamed [bold]{len(result.files_to_rename)}[/bold] files")
        console.print(f"Updated [bold]{result.number_of_links_changed}[/bold] links")

def display_rename_table(files_to_rename):
    table = Table(title="Files to be renamed")
    table.add_column("Original Filename", style="green", overflow="fold")
    table.add_column("New Filename", style="red", overflow="fold")
    for file in files_to_rename:
        table.add_row(file.old_base, file.new_base)
    console.print(table)
