data "aws_vpc" "default" {
  default = true
}

data "aws_subnets" "default" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }
}

data "aws_iam_role" "eks_cluster" {
  name = "LabEksClusterRole"
}

data "aws_iam_role" "eks_node" {
  name = "LabEksNodeRole"
}

locals {
  name       = "mecanica-siaes"
  subnet_ids = sort(data.aws_subnets.default.ids)
}
