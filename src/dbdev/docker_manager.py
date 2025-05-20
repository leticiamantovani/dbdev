import docker
import secrets
import string
from .logger import get_logger

logger = get_logger()

DB_IMAGES = {
    "mysql": {
        "env": ["MYSQL_ROOT_PASSWORD", "MYSQL_DATABASE", "MYSQL_USER", "MYSQL_PASSWORD"],
        "port": 3306,
    },
    "postgres": {
        "env": ["POSTGRES_PASSWORD", "POSTGRES_DB", "POSTGRES_USER"],
        "port": 5432,
    },
    "mariadb": {
        "env": ["MYSQL_ROOT_PASSWORD", "MYSQL_DATABASE", "MYSQL_USER", "MYSQL_PASSWORD"],
        "port": 3306,
    },
}

class DockerManager:
    def __init__(self):
        try:
            self.client = docker.from_env()
        except Exception as e:
            logger.error(f"Error connecting to Docker: {e}")
            raise

    def generate_password(self, length=12):
        return ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(length))

    def create_db(self, image, db_name, user, password, root_password):
        if image not in DB_IMAGES:
            raise ValueError(f"Image {image} not supported. Supported: {list(DB_IMAGES.keys())}")
        env_vars = []
        image_conf = DB_IMAGES[image]

        if "MYSQL_ROOT_PASSWORD" in image_conf["env"]:
            if not root_password:
                root_password = self.generate_password()
            env_vars.append(f"MYSQL_ROOT_PASSWORD={root_password}")
        if "POSTGRES_PASSWORD" in image_conf["env"]:
            if not root_password:
                root_password = self.generate_password()
            env_vars.append(f"POSTGRES_PASSWORD={root_password}")

        if "MYSQL_DATABASE" in image_conf["env"]:
            env_vars.append(f"MYSQL_DATABASE={db_name}")
        if "POSTGRES_DB" in image_conf["env"]:
            env_vars.append(f"POSTGRES_DB={db_name}")

        if "MYSQL_USER" in image_conf["env"]:
            env_vars.append(f"MYSQL_USER={user}")
            if not password:
                password = self.generate_password()
            env_vars.append(f"MYSQL_PASSWORD={password}")
        if "POSTGRES_USER" in image_conf["env"]:
            env_vars.append(f"POSTGRES_USER={user}")

        try:
            container = self.client.containers.run(
                image,
                name=db_name,
                detach=True,
                publish_all_ports = True,
                environment=env_vars,
                labels={"dbdev": "true"}
            )

            container_created = self.client.containers.get(container.id)
            host_port = container_created.ports.get("3306/tcp")[0].get("HostPort")

            logger.info(f"Database type: {image}")
            logger.info(f"Database Name: {db_name}")
            logger.info(f"Access Port: {host_port}")  
            logger.info(f"Root Password: {root_password}")
            if user:
                logger.info(f"User: {user}")
                logger.info(f"User Password: {password}")

            return container

        except Exception as e:
            logger.error(f"Failed to create database container: {e}")
            raise

    def list_dbs(self):
        containers = self.client.containers.list(filters={"label": "dbdev=true"})
        for container in containers:
            env_vars = container.attrs.get("Config", {}).get("Env", [])
            def get_env_var(var_name):
                for item in env_vars:
                    if item.startswith(f"{var_name}="):
                        return item.split("=", 1)[1]
                return None

            db_name = get_env_var("MYSQL_DATABASE") or get_env_var("POSTGRES_DB")
            if db_name:
                logger.info(f"ID: {container.id},\n Image: {container.image.tags},\n Status: {container.status},\n Database Name: {db_name}")
        return containers

    def remove_db(self, container_id):
        try:
            container = self.client.containers.get(container_id)
            container.remove(force=True)
            logger.info(f"Container {container_id} removed.")
        except Exception as e:
            logger.error(f"Failed to remove container {container_id}: {e}")
            raise

    def info(self, db_name):
        containers = self.client.containers.list(
            filters={
                "label": "dbdev=true",
                "name": db_name
            }
        )
        if not containers:
            logger.info(f"No containers found with name containing '{db_name}'.")
            return []

        for container in containers:
            logger.info(f"ID: {container.id},\n Image: {container.image.tags},\n Status: {container.status}")
            env_vars = container.attrs.get("Config", {}).get("Env", [])
            def get_env_var(var_name):
                for item in env_vars:
                    if item.startswith(f"{var_name}="):
                        return item.split("=", 1)[1]
                return None

            user = get_env_var("MYSQL_USER") or get_env_var("POSTGRES_USER")
            password = get_env_var("MYSQL_PASSWORD") or get_env_var("POSTGRES_PASSWORD")

            if user:
                logger.info(f"User: {user}")
            if password:
                logger.info(f"User Password: {password}")

        return containers

