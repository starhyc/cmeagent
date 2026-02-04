# SSH Key Management Procedures

## Overview

The system stores SSH credentials encrypted using Fernet symmetric encryption. This document outlines procedures for managing SSH credentials securely.

## Encryption Key Management

### Initial Setup

1. Generate a new Fernet key:
```python
from cryptography.fernet import Fernet
key = Fernet.generate_key()
print(key.decode())
```

2. Store the key in the `FERNET_KEY` environment variable
3. Restrict access to the `.env` file:
```bash
chmod 600 .env
chown www-data:www-data .env
```

### Key Rotation

Rotate the Fernet key quarterly or when:
- A team member with access leaves
- The key may have been compromised
- As part of regular security maintenance

**Rotation Procedure:**

1. Generate a new Fernet key
2. Create a migration script to re-encrypt all SSH passwords:
```python
from app.core.database import SessionLocal
from app.models.database import SSHServer
from cryptography.fernet import Fernet

old_key = "old-key-here"
new_key = "new-key-here"

old_cipher = Fernet(old_key.encode())
new_cipher = Fernet(new_key.encode())

db = SessionLocal()
servers = db.query(SSHServer).all()

for server in servers:
    decrypted = old_cipher.decrypt(server.encrypted_password.encode())
    server.encrypted_password = new_cipher.encrypt(decrypted).decode()

db.commit()
```

3. Update `FERNET_KEY` in environment
4. Restart the service

## SSH Server Configuration

### Adding SSH Servers

Only admin users can add SSH server configurations through the web interface or API.

**Required Information:**
- Server name (descriptive identifier)
- Hostname or IP address
- SSH port (default: 22)
- Username
- Password (encrypted at rest)
- Log file path on remote server

### Password vs SSH Keys

Current implementation uses password authentication. For enhanced security:

**Future Enhancement:** Support SSH key-based authentication
- Store private keys encrypted with Fernet
- Use paramiko's key-based authentication
- Rotate keys regularly

## Access Control

### Who Can Access SSH Credentials

- **Admin users**: Can add, view, and delete SSH server configurations
- **Regular users**: Cannot access SSH credentials
- **System**: Decrypts credentials only when collecting logs

### Audit Logging

All SSH-related operations are logged:
- Server configuration changes
- Log collection attempts
- Authentication failures

Review audit logs regularly:
```sql
SELECT * FROM audit_logs WHERE resource LIKE '%ssh%' ORDER BY timestamp DESC;
```

## Security Best Practices

1. **Principle of Least Privilege**: Create dedicated SSH users with minimal permissions
2. **Network Segmentation**: Restrict SSH access to specific IP ranges
3. **Connection Monitoring**: Monitor failed SSH attempts
4. **Regular Audits**: Review SSH server list quarterly
5. **Backup Encryption Keys**: Store Fernet key backup in secure key management system

## Incident Response

### If Encryption Key is Compromised

1. Immediately rotate the Fernet key
2. Review audit logs for unauthorized access
3. Change all SSH passwords on remote servers
4. Investigate how the key was compromised
5. Update security procedures to prevent recurrence

### If SSH Credentials are Compromised

1. Remove the compromised server from the system
2. Change the password on the remote server
3. Review logs for unauthorized log access
4. Re-add the server with new credentials

## Compliance

Ensure SSH credential management meets your organization's:
- Data protection policies
- Access control requirements
- Audit and logging standards
- Encryption standards
