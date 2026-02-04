import paramiko
from app.services.credentials import credential_manager
from app.models.database import SSHServer
import time

class SSHLogCollector:
    def __init__(self, server: SSHServer):
        self.server = server
        self.max_retries = 3
        self.base_delay = 1

    def collect_logs(self, remote_path: str, local_path: str):
        for attempt in range(self.max_retries):
            try:
                client = paramiko.SSHClient()
                client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

                password = credential_manager.decrypt(self.server.encrypted_password)
                client.connect(
                    hostname=self.server.host,
                    port=self.server.port,
                    username=self.server.username,
                    password=password,
                    timeout=30
                )

                sftp = client.open_sftp()
                sftp.get(remote_path, local_path)
                sftp.close()
                client.close()
                return True

            except Exception as e:
                if attempt < self.max_retries - 1:
                    delay = self.base_delay * (2 ** attempt)
                    time.sleep(delay)
                else:
                    raise e
