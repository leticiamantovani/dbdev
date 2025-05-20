import typer
from .docker_manager import DockerManager
from .logger import get_logger

app = typer.Typer()
logger = get_logger()

@app.command()
def create(
    image: str = typer.Option("mysql", help="Database image: mysql, postgres, mariadb"),
    db: str = typer.Option(..., help="Database name: "),
    user: str = typer.Option("myuser", help="Database user"),
    password: str = typer.Option("", help="Database user password"),
    root_password: str = typer.Option("", help="Root/admin password"),
):
    """
    Create a new database container.
    """
    manager = DockerManager()
    container = manager.create_db(image, db, user, password, root_password)
    logger.info(f"Container {container.id} created.")

@app.command()
def list():
    """
    List database containers.
    """
    manager = DockerManager()
    manager.list_dbs()

@app.command()
def remove(id: str):
    """
    Remove a database container by ID.
    """
    manager = DockerManager()
    manager.remove_db(id)

@app.command()
def info(db_name: str):
    """
    Get information about a database container by DB name.
    """
    manager = DockerManager()
    manager.info(db_name)

if __name__ == "__main__":
    app()
