import pytest
from dbdev.docker_manager import DockerManager

def test_generate_password():
    manager = DockerManager()
    pwd = manager.generate_password()
    assert isinstance(pwd, str)
    assert len(pwd) == 12
