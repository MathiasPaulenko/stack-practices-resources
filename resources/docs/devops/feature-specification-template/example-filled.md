# Feature Spec: Real-time Order Notifications

> Author: M. Paulenko | Product Owner: ______ | Status: Approved
> Created: 2026-01-12 | Last updated: 2026-01-20 | Target release: 2026-Q1
> Changelog: 2026-01-20 — added polling fallback after infra review

## Summary

Add real-time order status notifications to the user dashboard
using WebSocket connections. Users will see order updates
immediately without page refresh.

## Goals

- Reduce support tickets about order status by 30%
- Improve user engagement with the dashboard
- Provide sub-second notification delivery

## Non-Goals

- Mobile push notifications (separate feature)
- Email notifications (already implemented)
- Order history search (separate feature)

## User Stories

1. As a buyer, I want to see order status updates in real-time
   so I do not need to refresh the page.
2. As a seller, I want to know when an order is placed so I can
   prepare the shipment immediately.
3. As a support agent, I want to see the same notifications so I
   can answer customer questions accurately.

## Functional Requirements

- WebSocket connection on dashboard page load
- Reconnection with exponential backoff on disconnect
- Notification payload includes: order ID, status, timestamp
- Notifications appear as toast messages and in a notification panel

## Non-Functional Requirements

- Notification delivery latency: p95 < 500ms
- WebSocket connections: support 10,000 concurrent
- Fallback to polling if WebSocket fails after 3 retries
- Accessibility: notifications announced via ARIA live region

## Technical Approach

- WebSocket gateway: AWS API Gateway WebSocket
- Message broker: Redis Pub/Sub
- Auth: JWT token passed in connection query params
- Frontend: native WebSocket API with reconnection wrapper

## API Changes

- New endpoint: GET /api/v1/notifications/stream (WebSocket upgrade)
- New endpoint: GET /api/v1/notifications (REST fallback, polling)
- No breaking changes to existing endpoints

## Rollout Strategy

- Phase 1: Internal testing with 10 users (1 week)
- Phase 2: Beta with 5% of users (2 weeks)
- Phase 3: General availability (monitor for 1 week)
- Rollback: Disable WebSocket feature flag, users fall back to polling

## Acceptance Criteria

- [ ] WebSocket connects on dashboard load
- [ ] Order status changes appear within 500ms
- [ ] Connection recovers automatically after network interruption
- [ ] Notifications are accessible via screen reader
- [ ] System handles 10,000 concurrent connections in load test

## Approvals

| Role | Name | Decision | Date |
|------|------|----------|------|
| Product | M. Paulenko | Approved | 2026-01-20 |
| Engineering | ______ | Approved | 2026-01-20 |
| Design | ______ | Approved | 2026-01-19 |
| QA | ______ | Approved | 2026-01-20 |
