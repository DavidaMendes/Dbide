import subprocess

import typer

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
def runserver(port: str = typer.Argument("8000")):
    try:
        typer.echo(f"Iniciando servidor na porta {port}...")

        subprocess.run(
            ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", port, "--reload"], check=True
        )
    except subprocess.CalledProcessError as e:
        typer.echo(f"Erro ao rodar o servidor: {e}", err=True)

        raise typer.Exit(code=1)


@app.command()
def test():
    try:
        typer.echo("Realizando os testes...")

        subprocess.run(["coverage", "run", "tests.py"], check=True)
        subprocess.run(["coverage", "html"], check=True)
    except subprocess.CalledProcessError as e:
        typer.echo(f"Erro ao realizar os testes: {e}", err=True)

        raise typer.Exit(code=1)


@app.command()
def lint():
    try:
        typer.echo("Formatando os arquivos...")

        subprocess.run(
            ["ruff", "check", "--select", "I", "--fix", "--line-length", "99"], check=True
        )
        subprocess.run(["ruff", "format", "--line-length", "99"], check=True)
    except subprocess.CalledProcessError as e:
        typer.echo(f"Erro ao formatar os arquivos: {e}", err=True)

        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
