import typer
from rich import print
from cli import user

app = typer.Typer()

app.add_typer(user.app)

@app.command()
def hello(name: str, prompt = True):
    print(f"hello {name}")

if __name__ == '__main__':
    app()