resource "aws_security_group" "db" {
  name        = "${local.name}-mysql"
  description = "MySQL aberto para o laboratorio e para o EKS"
  vpc_id      = data.aws_vpc.default.id

  ingress {
    description = "MySQL"
    from_port   = 3306
    to_port     = 3306
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description     = "MySQL a partir do EKS"
    from_port       = 3306
    to_port         = 3306
    protocol        = "tcp"
    security_groups = [aws_eks_cluster.this.vpc_config[0].cluster_security_group_id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${local.name}-mysql"
  }
}

resource "aws_security_group_rule" "api_nodeport" {
  type              = "ingress"
  description       = "NodePort da API para o laboratorio"
  from_port         = 30100
  to_port           = 30100
  protocol          = "tcp"
  cidr_blocks       = ["0.0.0.0/0"]
  security_group_id = aws_eks_cluster.this.vpc_config[0].cluster_security_group_id
}
