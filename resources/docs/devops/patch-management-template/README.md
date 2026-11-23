# Patch Management Template — Companion

Files for the doc [Patch Management Template](https://stackpractices.com/docs/patch-management-template/).

- `patch-management-plan.md` — the copy-paste template (inventory, classification, checklist, schedule, verification, exception log).
- `patch-security-updates.yml` — Ansible playbook skeleton for rolling OS patching.
- `patch-image-pipeline.sh` — container base-image patch + Trivy scan + K8s rolling deploy.
