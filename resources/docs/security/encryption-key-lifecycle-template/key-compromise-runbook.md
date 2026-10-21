# Key Compromise Response Runbook

## 1. CONTAIN (immediate, 0-15 min)

- Disable the compromised key in KMS/HSM
- Revoke all access policies for the key
- Identify all data encrypted with the compromised key

## 2. ASSESS (15-60 min)

- Determine scope: which services, databases, backups affected
- Check access logs for unauthorized key usage
- Notify security team and key custodian

## 3. REPLACE (1-4 hours)

- Create new key with same policy
- Re-encrypt all affected data with new key
- Update application configurations to use new key ARN/ID
- Deploy updated configurations

## 4. DESTROY (after verification)

- Schedule deletion of compromised key
- Verify all data uses new key
- Document incident and update key inventory

## 5. POST-INCIDENT (within 1 week)

- Review root cause of compromise
- Update access policies and monitoring
- Conduct full key inventory audit
- Update key lifecycle documentation
