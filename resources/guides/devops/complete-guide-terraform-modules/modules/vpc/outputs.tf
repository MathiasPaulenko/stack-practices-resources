output "vpc_id" {
  description = "ID of the VPC"
  value       = aws_vpc.this.id
}

output "vpc_cidr_block" {
  description = "CIDR block of the VPC"
  value       = aws_vpc.this.cidr_block
}

output "public_subnet_ids" {
  description = "IDs of the public subnets, keyed by CIDR"
  value       = local.public_subnet_ids
}

output "private_subnet_ids" {
  description = "IDs of the private subnets, keyed by CIDR"
  value       = local.private_subnet_ids
}

output "nat_gateway_ip" {
  description = "Public IP of the NAT gateway (for allowlists)"
  value       = aws_eip.nat.public_ip
}
