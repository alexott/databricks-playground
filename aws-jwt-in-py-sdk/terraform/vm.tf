resource "aws_key_pair" "deployer" {
  key_name   = "${local.prefix}-key"
  public_key = file("~/.ssh/id_rsa.pub")
}

data "aws_ami" "ubuntu" {
  most_recent = true

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  owners = ["099720109477"] # Canonical
}

resource "aws_instance" "vm" {
  ami                         = data.aws_ami.ubuntu.id
  instance_type               = "i3.xlarge"
  key_name                    = aws_key_pair.deployer.key_name
  subnet_id                   = module.vpc.public_subnets[0]
  vpc_security_group_ids      = [aws_security_group.security.id]
  associate_public_ip_address = true
  tags                        = merge(var.tags, {Name="aott-splunk"})
  iam_instance_profile        = aws_iam_instance_profile.vm_profile.name

  root_block_device {
    volume_size = 64
  }
}

