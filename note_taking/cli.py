import typer
from rich.console import Console
from rich.table import Table
from file_operations import keyword_rename, handle_create_command
from models import RenameResult

console = Console()
app = typer.Typer()

@app.callback()
def callback():
    """
    Note Taking CLI based on PARA
    """

@app.command()
def create(keyword: str = typer.Argument(...),
           project: bool = typer.Option(False, "-p", "--project"),
           area: bool = typer.Option(False, "-a", "--area"),
           resource: bool = typer.Option(False, "-r", "--resource")):
    """
    Create files with the given keyword and flag.
    """
    handle_create_command(keyword, project, area, resource)

@app.command()
def rename(keyword: str = typer.Argument(...),
           replacement: str = typer.Argument(...),
           force: bool = typer.Option(False, "-f", "--force")):
    """
    Rename files with the given keyword and replacement and update all references to it.
    """
    result = keyword_rename(keyword, replacement, action=force)

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
        table.add_row(file['original'], file['change'])
    console.print(table)
