module "db" {
  source = "./modules/db"

  identifier        = local.name
  db_name           = var.mysql_database
  username          = var.mysql_user
  password          = var.mysql_password
  subnet_ids        = local.subnet_ids
  security_group_id = aws_security_group.db.id

  tags = {
    Name = "${local.name}-mysql"
  }
}
