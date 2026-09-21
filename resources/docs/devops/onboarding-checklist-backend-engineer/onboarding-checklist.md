# Backend Engineer Onboarding Checklist

## New Hire: ______ | Start Date: ______ | Manager: ______ | Buddy: ______

---

## Day 1: Welcome and Setup

### Administrative
- [ ] Complete HR paperwork and benefits enrollment
- [ ] Receive laptop and hardware setup
- [ ] Obtain building access badge / parking pass
- [ ] Set up email and calendar
- [ ] Join essential Slack/Teams channels
- [ ] Add profile photo and status to Slack
- [ ] Schedule 1:1s with manager, buddy, and team lead

### Development Environment
- [ ] Install required software (see engineering handbook for versions)
  - [ ] Git
  - [ ] Docker and Docker Compose
  - [ ] Node.js / Python / Java / Go (stack-specific)
  - [ ] IDE with team settings
  - [ ] kubectl and cloud CLI tools
  - [ ] Postman or API client
- [ ] Configure Git with company email and signing key
- [ ] Clone primary repositories
- [ ] Run the project locally following README instructions
- [ ] Verify local tests pass
- [ ] Make a trivial documentation fix and open first PR

### Access and Security
- [ ] Complete security awareness training
- [ ] Set up password manager with team vault access
- [ ] Enable MFA on all accounts (GitHub, cloud provider, VPN)
- [ ] Request and receive staging environment access
- [ ] Read and acknowledge data handling policies

---

## Week 1: Codebase Orientation

### Architecture and Systems
- [ ] Attend architecture overview session (recorded if unavailable live)
- [ ] Review system architecture diagram and data flow documentation
- [ ] Identify the 5 most critical services your team owns
- [ ] Understand the request lifecycle: client → load balancer → service → database
- [ ] Review API documentation (OpenAPI / Swagger)
- [ ] Run through the debugging guide for common local issues

### Code Standards
- [ ] Read team's coding standards document
- [ ] Review 5 recently merged PRs to understand review patterns
- [ ] Understand linting and formatting rules (run linters locally)
- [ ] Learn the team's testing philosophy (unit vs integration vs e2e)
- [ ] Review error handling patterns in the codebase

### Processes
- [ ] Understand the sprint/iteration rhythm (planning, standups, retros)
- [ ] Learn how to pick up work (ticket system, Kanban board)
- [ ] Attend sprint planning and retrospective as observer
- [ ] Understand on-call rotation and escalation procedures
- [ ] Review incident response runbooks

### First Contribution
- [ ] Pick up a "good first issue" (labeled in issue tracker)
- [ ] Open a PR following the team's PR template
- [ ] Receive and address code review feedback
- [ ] Merge first PR with buddy's guidance
- [ ] Verify change deploys to staging successfully

---

## Week 2: Deeper Integration

### Production Awareness
- [ ] Shadow an on-call engineer for one shift (non-interruptible)
- [ ] Review production monitoring dashboards
- [ ] Understand alerting thresholds and paging procedures
- [ ] Learn how to query logs in the team's log aggregation tool
- [ ] Review recent postmortems (last 3 months)

### Domain Knowledge
- [ ] Meet with product manager to understand current roadmap
- [ ] Review user-facing features and business logic with domain expert
- [ ] Understand data model and entity relationships
- [ ] Review integration points with external services
- [ ] Learn about compliance and regulatory requirements (if applicable)

### Ownership
- [ ] Identify the service or component you will own
- [ ] Review service ownership documentation
- [ ] Understand deployment pipeline for your service
- [ ] Learn rollback procedures for your service
- [ ] Add yourself to service on-call rotation (with supervision)

---

## Completion Verification

| Area | Verified By | Date | Notes |
|------|-------------|------|-------|
| Environment Setup | ______ | ______ | |
| Local Build Working | ______ | ______ | |
| First PR Merged | ______ | ______ | |
| Security Training | ______ | ______ | |
| Architecture Overview | ______ | ______ | |
| On-call Shadow Complete | ______ | ______ | |

## Feedback

**What was most helpful?**

**What was missing or confusing?**

**How long until you felt productive?**

**Recommendations for improving this checklist:**
