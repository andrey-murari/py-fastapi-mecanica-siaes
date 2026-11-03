resource "aws_eks_cluster" "this" {
  name     = local.name
  version  = "1.35"
  role_arn = local.eks_cluster_role_arn

  vpc_config {
    subnet_ids             = local.subnet_ids
    endpoint_public_access = true
    public_access_cidrs    = ["0.0.0.0/0"]
  }

  access_config {
    authentication_mode                         = "API_AND_CONFIG_MAP"
    bootstrap_cluster_creator_admin_permissions = true
  }

  tags = {
    Name = local.name
  }
}

resource "aws_eks_node_group" "this" {
  cluster_name    = aws_eks_cluster.this.name
  node_group_name = "default"
  node_role_arn   = local.eks_node_role_arn
  subnet_ids      = local.subnet_ids
  instance_types  = ["t3.small"]

  scaling_config {
    desired_size = 1
    min_size     = 1
    max_size     = 1
  }

  tags = {
    Name = "${local.name}-node"
  }
}

resource "aws_eks_addon" "this" {
  for_each = toset(["vpc-cni", "kube-proxy", "coredns"])

  cluster_name = aws_eks_cluster.this.name
  addon_name   = each.value

  depends_on = [aws_eks_node_group.this]
}
