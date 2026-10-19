# checkov_custom_policies/aws_require_tags.py
# Custom Checkov policy: every AWS resource must carry CostCenter + Environment tags.
# Run with: checkov -d terraform/ --external-checks-dir checkov_custom_policies/
from checkov.terraform.checks.resource.base_resource_check import BaseResourceCheck
from checkov.common.models.enums import CheckResult, CheckCategories


class RequireCostCenterTag(BaseResourceCheck):
    def __init__(self):
        name = "Ensure all resources have a CostCenter tag"
        check_id = "CKV_AWS_CUSTOM_1"
        supported_resources = ["aws_*"]
        categories = [CheckCategories.CONVENTION]
        super().__init__(name=name, id=check_id, categories=categories,
                         supported_resources=supported_resources)

    def scan_resource_conf(self, conf):
        tags = conf.get("tags", [{}])[0]
        if "CostCenter" in tags and "Environment" in tags:
            return CheckResult.PASSED
        return CheckResult.FAILED


check = RequireCostCenterTag()
