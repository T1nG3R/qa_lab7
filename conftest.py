import paramiko
import subprocess
import pytest
from config import server_ip, port, username, password


@pytest.fixture(scope='function')
def server():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=server_ip, port=port, username=username, password=password)

    stdin, stdout, stderr = ssh.exec_command("iperf3 -s -1")

    ssh.close()

    return ssh

@pytest.fixture(scope='function')
def client(server):
    client_command = f"iperf3 -c {server_ip}"
    result = subprocess.run(client_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    return result.stdout, result.stderr

