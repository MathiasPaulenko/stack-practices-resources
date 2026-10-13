import { Router, json } from 'express';

/**
 * CSP violation report endpoint.
 *
 * Accepts both payload shapes:
 * - Legacy report-uri:  {"csp-report": {...}}         (application/csp-report)
 * - Reporting API:      [{"type":"csp-violation","body":{...}}]  (application/reports+json)
 *
 * Register the Reporting API endpoint group in your headers with:
 *   Reporting-Endpoints: csp-endpoint="/api/csp-reports"
 */
export const cspReportRouter = Router();

interface CspReportBody {
  'document-uri'?: string;
  'effective-directive'?: string;
  'violated-directive'?: string;
  'blocked-uri'?: string;
  disposition?: string;
  'script-sample'?: string;
  [key: string]: unknown;
}

cspReportRouter.post(
  '/',
  json({ type: ['application/csp-report', 'application/reports+json'] }),
  (req, res) => {
    const payload = req.body;
    const reports: (CspReportBody | undefined)[] = Array.isArray(payload)
      ? payload.map((r) => r.body as CspReportBody)
      : [payload['csp-report'] as CspReportBody];

    for (const report of reports) {
      if (!report) continue;
      console.warn('CSP violation:', {
        documentUri: report['document-uri'],
        directive: report['effective-directive'] ?? report['violated-directive'],
        blockedUri: report['blocked-uri'],
        disposition: report.disposition,
        sample: report['script-sample'],
      });
    }

    res.status(204).end();
  },
);
