# Changelog

All notable changes to this module are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/) with semver versions.

## [2.3.1] - 2026-07-04

### Fixed
- Fixed IAM policy when `enable_logging` is false
- Fixed panic when `tags` is an empty map

## [2.3.0] - 2026-06-15

### Added
- New variable `enable_monitoring` (default: false)
- New output `monitoring_dashboard_url`

### Changed
- Updated AWS provider constraint to >= 5.0, < 6.0

## [2.2.0] - 2026-05-01

### Added
- Support for `kms_key_id` in the S3 bucket module

### Deprecated
- `instance_type` variable deprecated, use `instance_types` — removal scheduled for v3.0.0

## [2.0.0] - 2026-03-01

### Breaking
- `instance_type` removed, replaced with `instance_types` (list) — see MIGRATION-GUIDE.md
- `tags` output type changed from `map(string)` to `map(any)`
- Minimum Terraform version raised to 1.5
