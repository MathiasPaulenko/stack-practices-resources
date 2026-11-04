# Mixed on-demand + Spot Auto Scaling group and VPC endpoints.
# Apply with: terraform init && terraform apply

resource "aws_autoscaling_group" "spot" {
  mixed_instances_policy {
    instances_distribution {
      on_demand_base_capacity                  = 1
      on_demand_percentage_above_base_capacity = 0
      spot_allocation_strategy                 = "capacity-optimized"
    }

    launch_template {
      launch_template_specification {
        launch_template_id = aws_launch_template.app.id
        version            = "$Latest"
      }

      override {
        instance_type = "t3.medium"
      }
      override {
        instance_type = "t3.large"
      }
    }
  }

  min_size         = 2
  max_size         = 10
  desired_capacity = 4
}

# Gateway endpoint for S3 — free, removes NAT processing charges.
resource "aws_vpc_endpoint" "s3" {
  vpc_id          = aws_vpc.main.id
  service_name    = "com.amazonaws.us-east-1.s3"
  route_table_ids = [aws_route_table.private.id]
}

# Interface endpoint (~$0.01/hr) for frequently called AWS services.
resource "aws_vpc_endpoint" "dynamodb" {
  vpc_id            = aws_vpc.main.id
  service_name      = "com.amazonaws.us-east-1.dynamodb"
  vpc_endpoint_type = "Interface"
  subnet_ids        = aws_subnet.private[*].id
}
