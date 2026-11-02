resource "aws_db_subnet_group" "this" {
  name        = "${var.identifier}-subnets"
  description = "Subnets do MySQL da mecanica-siaes"
  subnet_ids  = var.subnet_ids

  tags = var.tags
}

resource "aws_db_instance" "this" {
  identifier     = var.identifier
  db_name        = var.db_name
  engine         = "mysql"
  engine_version = var.engine_version
  instance_class = var.instance_class

  username = var.username
  password = var.password

  allocated_storage = 20
  storage_type      = "gp3"
  storage_encrypted = true

  db_subnet_group_name   = aws_db_subnet_group.this.name
  vpc_security_group_ids = [var.security_group_id]
  publicly_accessible    = false
  multi_az               = false

  backup_retention_period = 0
  skip_final_snapshot     = true
  deletion_protection     = false
  apply_immediately       = true

  auto_minor_version_upgrade = false
  copy_tags_to_snapshot      = true

  tags = var.tags
}
