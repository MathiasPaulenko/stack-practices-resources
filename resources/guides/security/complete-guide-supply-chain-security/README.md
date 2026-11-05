# Complete Guide to Supply Chain Security — Companion

Runnable assets from the [Complete Guide to Supply Chain Security](https://stackpractices.com/guides/complete-guide-supply-chain-security/) on StackPractices.

## Files

| File | What it does |
| --- | --- |
| `sbom_validator.py` | Validates a CycloneDX SBOM: license compliance and outdated-component checks |
| `typosquat_detector.py` | Flags packages whose names look like typosquats/combosquats of popular packages |
| `generate_provenance.py` | Emits a SLSA v1.0 provenance attestation (in-toto statement) |
| `secure-build.yml` | Hardened GitHub Actions workflow: SHA-pinned actions, isolated build, sign + attest |
| `sca-pipeline.yml` | Software Composition Analysis pipeline: pip-audit, npm audit, Trivy, Snyk, SBOM |
| `npmrc.example` | `.npmrc` pinning scoped packages to an internal registry (dependency confusion) |
| `pip.conf.example` | `pip.conf` with internal index + explicit fallback; notes the virtual-repo option |
| `requirements-hashed.txt` | Example `requirements.txt` with `--hash` pins (`pip install --require-hashes`) |

## Usage

```bash
# Validate an SBOM
python sbom_validator.py sbom.json

# Check one package name for typosquatting
python typosquat_detector.py reqeusts

# Scan a requirements file
python typosquat_detector.py --scan requirements.txt

# Generate a SLSA v1.0 provenance statement
python generate_provenance.py

# Copy the workflows into your repo
cp secure-build.yml .github/workflows/
cp sca-pipeline.yml .github/workflows/

# Apply the dependency-confusion configs
cp npmrc.example .npmrc
cp pip.conf.example pip.conf
```

## Notes

- No dependencies beyond the Python stdlib for the three `.py` scripts.
- The workflows pin third-party actions to release tags or full commit SHAs — keep it that way.
- For SLSA L3 provenance, call `slsa-github-generator` as a job-level reusable workflow (see the commented `provenance` job in `secure-build.yml`), never inside `steps`.
