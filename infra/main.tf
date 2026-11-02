locals {
  registry   = "${data.aws_caller_identity.current.account_id}.dkr.ecr.${var.region}.amazonaws.com"
  image      = "${module.ecr.repository_url}:${var.image_tag}"
  subnet_ids = sort(data.aws_subnets.default.ids)
  api_env = join("\n", [
    "FOR_GET_ADDRESS=viacep",
    "FOR_STORING_DATA=mysql",
    "VIA_CEP_BASE_URL=https://viacep.com.br/ws/",
    "JWT_EXPIRE_MINUTES=60",
    "ADMIN_LOGIN=${var.admin_login}",
    "ADMIN_PASSWORD=${var.admin_password}",
    "JWT_SECRET=${var.jwt_secret}",
    "MYSQL_HOST=${module.db.address}",
    "MYSQL_PORT=${module.db.port}",
    "MYSQL_USER=${var.mysql_user}",
    "MYSQL_PASSWORD=${var.mysql_password}",
    "MYSQL_DATABASE=${var.mysql_database}",
    "",
  ])
}

module "ecr" {
  source = "./modules/ecr"

  name = var.ecr_repository_name
  tags = {
    Name = var.ecr_repository_name
  }
}

module "db" {
  source = "./modules/db"

  identifier        = "mecanica-siaes"
  db_name           = var.mysql_database
  engine_version    = var.mysql_engine_version
  instance_class    = var.db_instance_class
  username          = var.mysql_user
  password          = var.mysql_password
  subnet_ids        = local.subnet_ids
  security_group_id = aws_security_group.db.id
  tags = {
    Name = "mecanica-siaes-mysql"
  }
}

module "ec2" {
  source = "./modules/ec2"

  name                   = "mecanica-siaes-api"
  ami                    = data.aws_ami.ubuntu.id
  instance_type          = var.instance_type
  subnet_id              = local.subnet_ids[0]
  vpc_security_group_ids = [aws_security_group.api.id]
  user_data = replace(templatefile("${path.module}/templates/mecanica-api.sh.tftpl", {
    region       = var.region
    registry     = local.registry
    image        = local.image
    api_port     = 8000
    env_file_b64 = base64encode(local.api_env)
  }), "\r", "")
  tags = {
    Name = "mecanica-siaes-api"
  }
}
