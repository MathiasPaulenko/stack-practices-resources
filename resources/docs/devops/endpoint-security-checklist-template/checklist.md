# Endpoint Security Checklist

Copy-paste ready baseline for corporate devices. From the StackPractices template:
[Endpoint Device Security Checklist Template](https://stackpractices.com/docs/endpoint-security-checklist-template/)

## 1. Device Configuration

- [ ] Operating system is supported and receiving security updates.
- [ ] Automatic OS updates are enabled.
- [ ] Screen locks after a short period of inactivity.
- [ ] Strong password, PIN, or biometric authentication is required.
- [ ] Full-disk encryption is enabled.
- [ ] Built-in firewall is enabled.
- [ ] Guest or unused accounts are disabled.
- [ ] Remote wipe capability is configured.
- [ ] Device is registered in the MDM or endpoint management console.
- [ ] Location services are disabled or restricted to business needs.

## 2. Identity and Access

- [ ] Multi-factor authentication is enabled for all corporate accounts.
- [ ] Single sign-on (SSO) is used where possible.
- [ ] Local administrator privileges are restricted.
- [ ] Corporate credentials are never shared with personal accounts.
- [ ] Password manager is installed and configured.
- [ ] VPN or zero-trust client is required for remote access.

## 3. Software and Applications

- [ ] Only approved software is installed.
- [ ] Application whitelisting or store restrictions are enforced.
- [ ] Antivirus or EDR agent is installed and active.
- [ ] Web browser is updated with security extensions enabled.
- [ ] Unused or default applications are removed.
- [ ] Auto-updates are enabled for all business applications.

## 4. Network and Data Protection

- [ ] Public Wi-Fi access requires VPN.
- [ ] Bluetooth is disabled when not in use.
- [ ] USB and removable media use is restricted or monitored.
- [ ] Sensitive data is stored in approved cloud locations, not locally.
- [ ] Cloud sync services are restricted to corporate-approved tools.
- [ ] Backups are configured and encrypted.

## 5. Monitoring and Incident Response

- [ ] EDR agent is reporting to the security team.
- [ ] Device compliance status is visible in the management console.
- [ ] Alerts for lost or stolen devices are configured.
- [ ] Users know how to report a lost device or suspected compromise.
- [ ] Offboarding process revokes access and wipes corporate data.
