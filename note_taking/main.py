import os
import fileinput
import re
import typer
from rich.console import Console
from rich.table import Table
from pathlib import Path

console = Console()
app = typer.Typer()


@app.callback()
def callback():

    """
    Note Taking CLI based on PARA
    """

BASE_DIR = Path("/Users/nick/Documents/projects/GitHub/ndm_os/notes/")

# Custom Functions
def keyword_rename(keyword: str, replacement: str, action: bool = False):

    # Loop through all files in the directory
    ls_file_names = []
    number_of_links_change = 0
    for filename in os.listdir(BASE_DIR):
        change_flag = False
        if filename.endswith(".md"): # Check if the keyword is in the file name
            if keyword in filename:
                # Replace the keyword with the replacement word in the file name
                new_filename = filename.replace(keyword, replacement)
                change_dict = {"original": filename, "change": new_filename}
                ls_file_names.append(change_dict)
                change_flag = True
                if action:
                    # Rename the file
                    os.rename(os.path.join(BASE_DIR, filename), os.path.join(BASE_DIR, new_filename))
            
            if action:
                
                # Loop through each line in the file and change if matches
                if change_flag: # if the name was changed above then use the new name when searching for links inside the file
                    filename = new_filename
                with fileinput.FileInput(os.path.join(BASE_DIR, filename), inplace=True) as file:
                    # Loop through each line in the file
                    for line in file:
                        # Use regex to find all occurrences of the keyword inside double square brackets
                        pattern = re.compile(r'\[\[(.*?)\]\]')
                        matches = pattern.findall(line)
                        
                        # Loop through each match and replace the keyword with the replacement word
                        for match in matches:
                            new_match = match.replace(keyword, replacement)
                            if f"[[{match}]]" != f"[[{new_match}]]":
                                line = line.replace(f"[[{match}]]", f"[[{new_match}]]")
                                number_of_links_change += 1
                        
                        # Print the modified line to the file only if change was made
                        if line != file._backup:
                            print(line, end="")
                        # print(line, end="")
                # print(f"Updated links in {filename}")
    return(ls_file_names, number_of_links_change)


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
                file_name = f"{prefix}.{keyword}"
            else:
                file_name = f"{prefix}.{keyword}.{file_type}"
            file_path = BASE_DIR / f"{file_name}.md"
            file_path.touch(exist_ok=False)
            typer.echo(f"Created {file_name}")
        
@app.command()
def rename(keyword: str = typer.Argument(...),
           replacement: str = typer.Argument(...),
           force: bool = typer.Option(False, "-f", "--force")):
    """
    Rename files with the given keyword and replacement and update all references to it.
    """

    ls_file_names, links_updated = keyword_rename(keyword, replacement, action = force)

    if force == False: 
        table = Table(title="Files to be renamed")
        table.add_column("Original Filename", style="green" , overflow="fold")
        table.add_column("New Filename", style="red", overflow="fold")
        for file in ls_file_names:
            table.add_row(file['original'],file['change'] )
        console.print(table)
        console.print("[red]Please confirm the changes by running the command again with the[/red] [white]-f[/white] [red]flag")
    if force == True:
        console.print(f"Renamed [bold]{len(ls_file_names)}[/bold] files")
        console.print(f"Updated [bold]{links_updated}[/bold] links")



    
    