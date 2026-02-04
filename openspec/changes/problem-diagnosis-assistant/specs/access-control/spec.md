## ADDED Requirements

### Requirement: Implement role-based access control
The system SHALL support admin and user roles with different permission levels.

#### Scenario: Admin role capabilities
- **WHEN** admin user logs in
- **THEN** user has access to all features including configuration, user management, and sensitive code

#### Scenario: User role restrictions
- **WHEN** regular user logs in
- **THEN** user can view and analyze but cannot access configuration or sensitive code modules

#### Scenario: Role assignment
- **WHEN** admin creates new user account
- **THEN** admin can assign either admin or user role

### Requirement: Control access to sensitive code
The system SHALL restrict access to designated sensitive code modules based on user role.

#### Scenario: Sensitive code restriction
- **WHEN** regular user attempts to view sensitive code module
- **THEN** system denies access and shows permission error

#### Scenario: Admin code access
- **WHEN** admin user views any code module
- **THEN** system grants access including sensitive modules

#### Scenario: Sensitive module configuration
- **WHEN** admin marks code module as sensitive
- **THEN** system restricts access to that module for regular users

### Requirement: Control SSH server access
The system SHALL restrict SSH server configuration and usage based on user role.

#### Scenario: User SSH restrictions
- **WHEN** regular user attempts to configure SSH servers
- **THEN** system denies access to SSH configuration

#### Scenario: Admin SSH access
- **WHEN** admin user configures SSH servers
- **THEN** system allows configuration and credential management

#### Scenario: User log collection
- **WHEN** regular user collects logs
- **THEN** user can only use pre-configured SSH servers, not add new ones

### Requirement: Maintain audit logs
The system SHALL record all user operations with timestamp, user, action, and target.

#### Scenario: Operation logging
- **WHEN** user performs any action (upload, analyze, export, configure)
- **THEN** system records audit log entry with user ID, timestamp, action type, and affected resources

#### Scenario: Audit log query
- **WHEN** admin views audit logs
- **THEN** system displays all operations with filtering by user, date range, and action type

#### Scenario: Audit log export
- **WHEN** admin exports audit logs
- **THEN** system generates downloadable file with all audit entries

### Requirement: Session management
The system SHALL implement 30-minute session timeout for inactive users.

#### Scenario: Session timeout
- **WHEN** user is inactive for 30 minutes
- **THEN** system automatically logs out user and requires re-authentication

#### Scenario: Session activity tracking
- **WHEN** user performs any action
- **THEN** system resets inactivity timer

#### Scenario: Timeout warning
- **WHEN** user approaches session timeout (e.g., 28 minutes)
- **THEN** system shows warning notification

### Requirement: Secure credential storage
The system SHALL encrypt SSH passwords and API keys at rest.

#### Scenario: Password encryption
- **WHEN** admin saves SSH password
- **THEN** system encrypts password before storing in database

#### Scenario: Password retrieval
- **WHEN** system needs to use SSH password
- **THEN** system decrypts password securely without exposing it in logs or UI

#### Scenario: Encryption key management
- **WHEN** system starts
- **THEN** system loads encryption key from secure environment variable

### Requirement: Authentication
The system SHALL require username and password authentication for all users.

#### Scenario: User login
- **WHEN** user enters valid credentials
- **THEN** system authenticates user and creates session

#### Scenario: Invalid credentials
- **WHEN** user enters invalid credentials
- **THEN** system denies access and shows error message

#### Scenario: Password requirements
- **WHEN** admin creates user account
- **THEN** system enforces minimum password complexity requirements
