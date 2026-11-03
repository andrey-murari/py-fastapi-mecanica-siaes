resource "aws_ecr_repository" "this" {
  name                 = "fiap-17soat/siaes-ci-cd"
  image_tag_mutability = "MUTABLE"
  force_delete         = true

  tags = {
    Name = "fiap-17soat/siaes-ci-cd"
  }
}

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
