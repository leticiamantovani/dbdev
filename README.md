# Dbdev

**Dbdev** is a powerful CLI tool that helps developers easily create, list, and manage SQL database containers using Docker. It supports multiple database engines (MySQL, PostgreSQL, MariaDB, and more), generates secure credentials, and is built for easy local development. The tool can be used via PyPI, via Docker, or with Docker Compose.

## 🔗 Library link

[![PyPI](https://img.shields.io/pypi/v/dbdev.svg)](https://pypi.org/project/dbdev/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![Docker](https://img.shields.io/badge/docker-20.10%2B-blue.svg)](https://docs.docker.com/get-docker/)
[![GitHub Issues](https://img.shields.io/github/issues/leticiamantovani/dbdev.svg)](https://github.com/leticiamantovani/dbdev/issues)

---

## 🚀 Features

* **Easy CLI:** Create, list, and remove database containers from the command line
* **Multi-DB Support:** MySQL, PostgreSQL, MariaDB (and easily extensible)
* **Secure Credentials:** Generates strong, random passwords
* **Configurable:** Use environment variables and `.env` files
* **Logging & Error Handling:** Robust, production-oriented output
* **Extensible:** Modular Python code ready for new features
* **Docker-Ready:** Can be used as a local CLI, via PyPI, also via Docker, or via Docker Compose

---

## 📦 Requirements

* **Docker:** Must be installed and **running** on your machine

  * [Get Docker here](https://docs.docker.com/get-docker/)
* **Python 3.8+** (for using the library/CLI via PyPI/pip)

---

## 🔧 How can I use?

**Note:**

* The CLI uses your local Docker daemon to manage database containers.
* Docker **must be installed and running** on your machine.
* The library does NOT install or manage Docker itself.

---

---

### Run via PyPI (Easiest way) 

1. **Ensure Docker is installed and running on your machine.**

2. **Install the CLI globally or in a virtual environment:**

   ```bash
   pip install dbdev
   ```

3. **Use the CLI:**

   ```bash
   dbdev --help
   dbdev create --image mysql --db testdb --user myuser
   dbdev list
   dbdev remove --id <container_id>
   ```

---

**Tip:**
If you encounter permission errors, you may need to run Docker with `sudo` (Linux) or ensure your user is in the `docker` group.

---

### Run Locally (Development Mode)

1. **Clone the repository:**

   ```bash
   git clone https://github.com/leticiamantovani/dbdev.git
   cd dbdev
   ```

2. **(Recommended) Create and activate a virtual environment:**

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate      # On Windows: .venv\Scripts\activate
   ```

3. **Install the package in editable mode (and pytest for testing):**

   ```bash
   pip install -e .
   pip install pytest
   ```

4. **Ensure Docker is installed and running on your machine.**

5. **Use the CLI:**

   ```bash
   dbdev --help
   dbdev create --image mysql --db testdb --user myuser
   dbdev list
   dbdev remove --id <container_id> OR <db_name>
   ```

### Run via Docker

If you prefer not to install Python or dependencies, you can use the CLI directly from a Docker container.

**Build the Docker image:**

```bash
docker build -t dbdev:v1 .
```

**Important:**

* The volume flag `-v /var/run/docker.sock:/var/run/docker.sock` is **required** to let the CLI inside the container access your host's Docker service. Without it, you will get connection errors like:

  > `DockerException: Error while fetching server API version: ('Connection aborted.', FileNotFoundError(2, 'No such file or directory'))`

---

**Run a command (example: list containers):**

```bash
docker run --rm -it \
  -v /var/run/docker.sock:/var/run/docker.sock \
  dbdev:v1 list
```

### Run via Docker Compose

**How to use:**

1. Place the `docker-compose.yml` file in your project root.
2. Build and start the service:

   ```bash
   docker-compose up --build
   ```

   This shows the CLI help and, if set up with a custom entrypoint, drops you into a shell for debugging.
3. To use the CLI for specific commands (recommended):

   ```bash
   docker-compose run --rm dbdev list
   docker-compose run --rm dbdev create --image mysql --db testdb --user myuser
   ```

---

## ⚡ Commands

### Show help

```bash
dbdev --help
# or
python -m dbdev.cli --help
```

### Create a new database container

```bash
dbdev create --image mysql --db mydb --user devuser --password mypass --root-password rootpass
```

* `--image`: Database image (mysql, postgres, mariadb) [DEFAULT: mysql]
* `--db`: Name of the database to create [REQUIRED]
* `--user`: Database user [OPTIONAL, random if not provided]
* `--password`: User's password [OPTIONAL, random if not provided]
* `--root-password`: Root/admin password [OPTIONAL, random if not provided]

### List all managed containers

```bash
dbdev list
```

### Get details of a specific container

```bash
dbdev info <db_name>
```

* `db_name`: Name of the database to create [REQUIRED]

### Remove a database container

```bash
dbdev remove <container_id> 
# or
dbdev remove <db_name>
```

* `container_id`: ID of the container to remove [REQUIRED]
* `db_name`: Name of the database to create [REQUIRED]

---

## ⚙️ Configuration

You can use a `.env` file to set default values (automatically loaded if present):

```
DEFAULT_DB_IMAGE=mysql
DEFAULT_DB_PORT=3306
```

---

## 🐳 Supported Database Images

* **MySQL** (default)
* **PostgreSQL**
* **MariaDB**

Want support for another image? Open a pull request or submit a feature request!

---

## 🛠️ Development & Contribution

Contributions are welcome! To set up for local development:

```bash
git clone https://github.com/leticiamantovani/dbdev.git
cd dbdev
pip install -e .
pip install pytest
```

To run the tests:

```bash
pytest tests/
```

To add a new database image:

* Edit `src/dbdev/docker_manager.py`, and add the image config in `DB_IMAGES`.

Open an issue or pull request with your improvements or bug reports.

---

## 🚨 Troubleshooting

* **Docker not installed/running:**
  Make sure Docker is installed and running on your machine before using the CLI.
* **Permission denied on docker.sock:**
  On Linux, you might need to add your user to the `docker` group or use `sudo`.
* **Docker socket not available in the container:**

  * Always run with `-v /var/run/docker.sock:/var/run/docker.sock` to allow the CLI inside the container to control your host's Docker daemon.
* **PyPI install notes:**

  * The library only manages Docker containers using your local Docker service. It will not install Docker for you. Make sure Docker is running on your machine before using any CLI commands.

---

## 📝 License

MIT License. See [LICENSE](LICENSE) for details.

---

## ⭐ Credits

Created by [Leticia Mantovani](https://github.com/leticiamantovani).
Contributions, feedback, and issues are very welcome!

---

> *If you use and like this project, please give it a ⭐ on GitHub!*
