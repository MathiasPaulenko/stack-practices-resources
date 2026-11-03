# Self-Hosted Runner Hardening Checklist

- [ ] Runner isolated in a VPC with no direct internet egress (or an egress proxy with allowlist)
- [ ] Separate runner pools per team or trust level — never share pools between apps
- [ ] Runner user has no sudo/root; container builds run rootless
- [ ] /tmp mounted as `noexec,nodev,nosuid`
- [ ] Workspace wiped between jobs — no reuse of build directories
- [ ] Runner images scanned weekly for CVEs and rebuilt on a schedule
- [ ] No long-lived secrets on disk; credentials injected at runtime only (tmpfs)
- [ ] Audit logging enabled: who ran what job, when, with what credentials
- [ ] Consider ephemeral runners (K8s jobs, autoscaled) instead of persistent VMs
