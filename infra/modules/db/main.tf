resource "aws_db_subnet_group" "this" {
  name       = "${var.identifier}-subnets"
  subnet_ids = var.subnet_ids
  tags       = var.tags
}

resource "aws_db_instance" "this" {
  identifier     = var.identifier
  db_name        = var.db_name
  engine         = "mysql"
  engine_version = "8.0"
  instance_class = "db.t3.micro"

  username = var.username
  password = var.password

  allocated_storage = 20

  db_subnet_group_name   = aws_db_subnet_group.this.name
  vpc_security_group_ids = [var.security_group_id]
  publicly_accessible    = true

  backup_retention_period = 0
  skip_final_snapshot     = true
  apply_immediately       = true

  tags = var.tags
}
