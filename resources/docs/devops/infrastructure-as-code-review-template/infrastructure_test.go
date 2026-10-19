// test/infrastructure_test.go
// Terratest: apply the VPC module in a test account and assert on the outputs.
// Requires AWS credentials with permission to create VPC resources.
package test

import (
	"testing"
	"time"

	"github.com/gruntwork-io/terratest/modules/aws"
	"github.com/gruntwork-io/terratest/modules/terraform"
	"github.com/stretchr/testify/assert"
)

func TestVpcModule(t *testing.T) {
	terraformOptions := &terraform.Options{
		TerraformDir: "../terraform/modules/vpc",
		Vars: map[string]interface{}{
			"environment": "test",
			"vpc_cidr":    "10.0.0.0/16",
			"enable_nat":  true,
		},
	}

	defer terraform.Destroy(t, terraformOptions)
	terraform.InitAndApply(t, terraformOptions)

	vpcId := terraform.Output(t, terraformOptions, "vpc_id")
	assert.NotEmpty(t, vpcId)

	subnetIds := terraform.OutputList(t, terraformOptions, "private_subnet_ids")
	assert.Equal(t, 2, len(subnetIds))

	// Verify NAT gateway was created
	natGatewayId := terraform.Output(t, terraformOptions, "nat_gateway_id")
	assert.NotEmpty(t, natGatewayId)

	// Verify VPC has DNS support
	aws.AssertVpcDnsSupportEnabled(t, "us-east-1", vpcId)
}
