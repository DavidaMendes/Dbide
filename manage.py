import typer
import subprocess

app = typer.Typer()


@app.command()
def makemigrations(message: str):
    try:
        subprocess.run(["alembic", "revision", "--autogenerate", "-m", message], check=True)

        typer.echo(f"Migração criada com sucesso: {message}")
    except subprocess.CalledProcessError as e:
        typer.echo(f"Erro ao criar migração: {e}", err=True)

        raise typer.Exit(code=1)


@app.command()
def migrate():
    try:
        subprocess.run(["alembic", "upgrade", "head"], check=True)

        typer.echo("Migrações aplicadas com sucesso.")
    except subprocess.CalledProcessError as e:
        typer.echo(f"Erro ao aplicar migrações: {e}", err=True)

        raise typer.Exit(code=1)


@app.command()
def runserver(port: str):
    try:
        subprocess.run(
            ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", port, "--reload"], check=True
        )
    except subprocess.CalledProcessError as e:
        typer.echo(f"Erro ao rodar o servidor: {e}", err=True)

        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
