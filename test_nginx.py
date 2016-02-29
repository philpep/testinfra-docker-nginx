import requests


def test_nginx_package(Package):
    pkg = Package("nginx")
    assert pkg.is_installed
    assert pkg.version == "1.4.6-1ubuntu3.4"


def test_nginx_socket(Socket):
    socket = Socket("tcp://80")
    assert socket.is_listening


def test_nginx_process(Process):
    master = Process.get(pid=1)
    assert master.args == "nginx: master process nginx"
    workers = Process.filter(ppid=master.pid)
    assert len(workers) == 4


def test_http_request(docker_ip):
    response = requests.get("http://" + docker_ip)
    assert response.status_code == 200
    assert "Welcome to nginx!" in response.content
