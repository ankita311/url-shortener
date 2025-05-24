import typer
from rich import print
from rich.console import Console
from rich.spinner import Spinner
import httpx
from . import utils

app = typer.Typer()
console = Console()

API_BASE_USER = "http://localhost:8000/user"
API_BASE_LOG = "http://localhost:8000"

@app.command(help="Register user")
def register(full_name: str = typer.Option(..., prompt=True, help="The name of the user"),
             email: str = typer.Option(..., prompt=True, help="The email of the user"),
             password: str = typer.Option(..., prompt=True, help="The password of the user")):
    
    try:
        r = httpx.post(f"{API_BASE_USER}/register",
                          json={"full_name": full_name, "email": email, "password": password})
        r.raise_for_status()

    except httpx.HTTPStatusError as e:
        print(f"[red] HTTP error {e.r.status_code}: {e.r.text}[/red]")
        raise typer.Exit(code=1)
    except httpx.RequestError as e:
        print(f"[red] Network error: {e}[/red]")
        raise typer.Exit(code=1)
    
    print(r.json())

@app.command(help="Login")
def login(email: str = typer.Option(..., prompt=True, help="Email of the user"),
          password: str = typer.Option(..., prompt=True, help="Password of the user")):
    
    data = {
        "username": email,
        "password": password
    }

    try:
        with console.status("[bold green]Logging in...", spinner="dots") as status:
            r = httpx.post(f"{API_BASE_LOG}/login", data=data, timeout=10)

        if r.status_code == 200:
            token = r.json()["access_token"]
            token_path = utils.get_token_path()
            token_path.parent.mkdir(parents=True, exist_ok=True)
            token_path.write_text(token)
            print("[green]Login Successfull![/green]")
        else:
            print(f"[red]Login failed: {r.json()['detail']}[/red]")

    except httpx.RequestError as e:
        print(f"[red]Request error {e}[/red]")


@app.command(help="Show user profile")
def profile():
    #logging logic
    token = utils.get_saved_token()

    if not token:
        print("[red]You are not logged in. Please log in to continue[/red]")
        raise typer.Exit()
    
    headers ={"Authorization": f"Bearer {token}"}

    with console.status("[bold green]Fetching Profile...") as status:
        r = httpx.get(f"{API_BASE_USER}/profile", headers=headers)

    if r.status_code == 401:
        print('[red]Sesson expired or invalid token. Please login again.[/red]')
        utils.delete_token()
        raise typer.Exit()

    if r.status_code != 200:
        print(f"[red]Error: {r.status_code} - {r.text}[/red]")
        raise typer.Exit()
    
    #main logic
    user = r.json()
    print("Your Profile- ")
    for k, v in user.items():
        print(f"{k}: {v}")
