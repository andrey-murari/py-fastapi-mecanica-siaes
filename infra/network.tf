resource "aws_security_group" "api" {
  name        = "mecanica-siaes-api"
  description = "HTTP da API FastAPI na porta 8000"
  vpc_id      = data.aws_vpc.default.id

  ingress {
    description = "API"
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = [var.api_ingress_cidr]
  }

  egress {
    description = "Saida para ECR, RDS e ViaCEP"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "mecanica-siaes-api"
  }
}

resource "aws_security_group" "db" {
  name        = "mecanica-siaes-mysql"
  description = "MySQL acessivel somente pela instancia da API"
  vpc_id      = data.aws_vpc.default.id

  ingress {
    description     = "MySQL a partir da API"
    from_port       = 3306
    to_port         = 3306
    protocol        = "tcp"
    security_groups = [aws_security_group.api.id]
  }

  egress {
    description = "Saida"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "mecanica-siaes-mysql"
  }
}
