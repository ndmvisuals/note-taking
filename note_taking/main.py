import os
import typer
from pathlib import Path


app = typer.Typer()


@app.callback()
def callback():

    """
    Note Taking CLI based on PARA
    """

BASE_DIR = Path("/Users/nick/Documents/projects/GitHub/ndm_os/notes/")


@app.command()
def create(keyword: str =  typer.Argument(...),
                project: bool = typer.Option(False, "-p", "--project"),
                area: bool = typer.Option(False, "-a", "--area"),
                resource: bool = typer.Option(False, "-r", "--resource")):
    """
    Create files with the given keyword and flag.
    """
    if sum([project, area, resource]) > 1:
        typer.echo("Please provide only one flag (-p, -a, -r)")
        return
    elif sum([project, area, resource]) == 0:
        typer.echo("Please provide one flag (-p, -a, -r)")
        return
    else:
        if project:
            prefix = "project"
            file_types = [keyword,'todo', 'note', 'meeting', 'log', "links"]
            
        elif area:
            prefix = "area"
            file_types = [keyword,'todo', 'note', 'meeting', 'log', "links"]
        elif resource:
            prefix = "resource"
            file_types = [keyword,"links"]

        for file_type in file_types:
            if file_type == keyword:
                file_name = f"{prefix}.{keyword}.md"
            else:
                file_name = f"{prefix}.{keyword}.{file_type}"
            file_path = BASE_DIR / f"{file_name}.md"
            file_path.touch(exist_ok=False)
            typer.echo(f"Created {file_name}")
        

    