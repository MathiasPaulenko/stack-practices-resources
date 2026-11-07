package test

import (
	"testing"

	"github.com/gruntwork-io/terratest/modules/terraform"
	"github.com/stretchr/testify/assert"
)

// Deploys modules/vpc/examples/basic for real and asserts on live outputs.
// Requires AWS credentials and ~$ of NAT gateway cost; run manually or on release.
func TestVpcModule(t *testing.T) {
	terraformOptions := &terraform.Options{
		TerraformDir: "../modules/vpc/examples/basic",
		Vars: map[string]interface{}{
			"name":       "terratest-vpc",
			"cidr_block": "10.99.0.0/16",
		},
	}

	defer terraform.Destroy(t, terraformOptions)
	terraform.InitAndApply(t, terraformOptions)

	vpcID := terraform.Output(t, terraformOptions, "vpc_id")
	assert.NotEmpty(t, vpcID)

	publicSubnets := terraform.OutputList(t, terraformOptions, "public_subnet_ids")
	assert.Len(t, publicSubnets, 2)
}
