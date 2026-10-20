// Audit a GitHub organization: list members, flag users without 2FA and admins.
// Requires: npm install @octokit/rest
// Usage:
//   GITHUB_TOKEN=ghp_xxx node github-org-audit.js your-org

const { Octokit } = require("@octokit/rest");

async function auditGitHubOrg(orgName, token) {
  const octokit = new Octokit({ auth: token });
  const findings = [];

  // Get all organization members
  const members = await octokit.paginate(
    octokit.rest.orgs.listMembers,
    { org: orgName, per_page: 100 }
  );

  // Members with 2FA disabled — a dedicated API filter;
  // the flag is not part of the default member payload
  const no2faMembers = await octokit.paginate(
    octokit.rest.orgs.listMembers,
    { org: orgName, filter: "2fa_disabled", per_page: 100 }
  );
  const no2faLogins = new Set(no2faMembers.map((m) => m.login));

  for (const member of members) {
    // Get the user's org role via the membership endpoint
    const { data: membership } = await octokit.rest.orgs.getMembershipForUser({
      org: orgName,
      username: member.login,
    });

    findings.push({
      login: member.login,
      role: membership.role,
      two_factor: no2faLogins.has(member.login) ? "disabled" : "enabled",
    });
  }

  // Flag users without 2FA
  const noMfa = findings.filter((f) => f.two_factor === "disabled");
  if (noMfa.length > 0) {
    console.log(`\nUSERS WITHOUT 2FA (${noMfa.length}):`);
    noMfa.forEach((u) => console.log(`  - ${u.login} (role: ${u.role})`));
  }

  // Flag admins
  const admins = findings.filter((f) => f.role === "admin");
  console.log(`\nORGANIZATION ADMINS (${admins.length}):`);
  admins.forEach((u) => console.log(`  - ${u.login} (2FA: ${u.two_factor})`));

  return findings;
}

const org = process.argv[2];
if (!org) {
  console.error("Usage: GITHUB_TOKEN=xxx node github-org-audit.js <org>");
  process.exit(1);
}

auditGitHubOrg(org, process.env.GITHUB_TOKEN)
  .then(() => console.log("\nAudit complete."))
  .catch((err) => {
    console.error("Audit failed:", err.message);
    process.exit(1);
  });
