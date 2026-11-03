data "aws_vpc" "default" {
  default = true
}

data "aws_subnets" "default" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }

  filter {
    name   = "availability-zone"
    values = ["us-east-1a", "us-east-1b", "us-east-1c", "us-east-1d", "us-east-1f"]
  }
}

data "aws_iam_roles" "eks_cluster" {
  name_regex = "LabEksClusterRole"
}

data "aws_iam_roles" "eks_node" {
  name_regex = "LabEksNodeRole"
}

locals {
  name                 = "mecanica-siaes"
  subnet_ids           = sort(data.aws_subnets.default.ids)
  eks_cluster_role_arn = one(data.aws_iam_roles.eks_cluster.arns)
  eks_node_role_arn    = one(data.aws_iam_roles.eks_node.arns)
}
