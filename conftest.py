import pytest
import testinfra


@pytest.fixture(scope="module")
def _docker_build(LocalCommand):
    LocalCommand("docker build -t testinfra-nginx .")


@pytest.fixture()
def Docker(_docker_build, request, LocalCommand):
    docker_id = LocalCommand.check_output("docker run -d testinfra-nginx")

    def teardown():
        LocalCommand.check_output("docker kill %s", docker_id)
        LocalCommand.check_output("docker rm %s", docker_id)

    request.addfinalizer(teardown)
    return testinfra.get_backend("docker://" + docker_id)


@pytest.fixture()
def docker_ip(Docker, LocalCommand):
    return LocalCommand.check_output(
        "docker inspect --format '{{ .NetworkSettings.IPAddress }}' %s",
        Docker.get_hostname(),
    )


@pytest.fixture()
def Package(Docker):
    return Docker.get_module("Package")


@pytest.fixture()
def Socket(Docker):
    return Docker.get_module("Socket")
