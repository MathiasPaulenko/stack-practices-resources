"""Scheduled Terraform drift detection with email alerting.

Runs init + refresh + plan -detailed-exitcode per environment and emails
the platform team when an environment drifts from its Terraform code.
"""
import subprocess
import smtplib
from email.mime.text import MIMEText
from typing import List, Dict


class DriftDetector:
    def __init__(self, terraform_dir: str, environments: List[str]):
        self.terraform_dir = terraform_dir
        self.environments = environments

    def check_drift(self, env: str) -> Dict:
        """Check for drift in a specific environment."""
        result = {"environment": env, "drifted": False, "resources": []}
        env_dir = f"{self.terraform_dir}/{env}"

        try:
            subprocess.run(
                ["terraform", f"-chdir={env_dir}", "init", "-input=false"],
                check=True, capture_output=True
            )
            subprocess.run(
                ["terraform", f"-chdir={env_dir}", "refresh", "-input=false"],
                check=True, capture_output=True
            )
            plan = subprocess.run(
                ["terraform", f"-chdir={env_dir}", "plan", "-detailed-exitcode", "-input=false"],
                capture_output=True, text=True
            )

            if plan.returncode == 2:
                result["drifted"] = True
                result["resources"] = self._parse_drifted_resources(plan.stdout)
        except subprocess.CalledProcessError as e:
            result["error"] = str(e)

        return result

    def _parse_drifted_resources(self, plan_output: str) -> List[str]:
        """Extract resource addresses from plan output."""
        resources = []
        for line in plan_output.split("\n"):
            if line.startswith("  # ") and "will be" in line:
                resources.append(line.strip())
        return resources

    def send_alert(self, drift_results: List[Dict]) -> None:
        """Send email alert if drift is detected."""
        drifted_envs = [r for r in drift_results if r["drifted"]]
        if not drifted_envs:
            return

        body = "Drift detected in the following environments:\n\n"
        for env in drifted_envs:
            body += f"Environment: {env['environment']}\n"
            for resource in env["resources"]:
                body += f"  - {resource}\n"
            body += "\n"

        msg = MIMEText(body)
        msg["Subject"] = "[ALERT] Terraform Drift Detected"
        msg["From"] = "infra-alerts@example.com"
        msg["To"] = "platform-team@example.com"

        with smtplib.SMTP("smtp.example.com", 587) as server:
            server.send_message(msg)


# Example usage
detector = DriftDetector("terraform/environments", ["prod", "staging", "dev"])
results = [detector.check_drift(env) for env in detector.environments]
detector.send_alert(results)
