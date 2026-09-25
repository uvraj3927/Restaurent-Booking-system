# ==============================================================================
# 1. PROVIDER CONFIGURATION
# ==============================================================================
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "us-east-1" # Change to your preferred AWS region
}

# ==============================================================================
# 2. VPC & INTERNET GATEWAY
# ==============================================================================
resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name = "custom-app-vpc"
  }
}

resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "app-igw"
  }
}

# ==============================================================================
# 3. SUBNETS
# ==============================================================================
# Public Subnet for EC2 App Server
resource "aws_subnet" "public_subnet" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.1.0/24"
  availability_zone       = "us-east-1a"
  map_public_ip_on_launch = true

  tags = {
    Name = "public-subnet-1"
  }
}

# Private Subnet 1 for RDS
resource "aws_subnet" "private_subnet_1" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.2.0/24"
  availability_zone = "us-east-1a"

  tags = {
    Name = "private-subnet-1"
  }
}

# Private Subnet 2 for RDS (Required by AWS RDS for Multi-AZ coverage)
resource "aws_subnet" "private_subnet_2" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.3.0/24"
  availability_zone = "us-east-1b"

  tags = {
    Name = "private-subnet-2"
  }
}

# ==============================================================================
# 4. ROUTE TABLES
# ==============================================================================
# Route Table for Public Subnet (Routes Internet Traffic via IGW)
resource "aws_route_table" "public_rt" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.igw.id
  }

  tags = {
    Name = "public-route-table"
  }
}

resource "aws_route_table_association" "public_assoc" {
  subnet_id      = aws_subnet.public_subnet.id
  route_table_id = aws_route_table.public_rt.id
}

# Private Route Table (Isolated from the Internet)
resource "aws_route_table" "private_rt" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "private-route-table"
  }
}

resource "aws_route_table_association" "private_assoc_1" {
  subnet_id      = aws_subnet.private_subnet_1.id
  route_table_id = aws_route_table.private_rt.id
}

resource "aws_route_table_association" "private_assoc_2" {
  subnet_id      = aws_subnet.private_subnet_2.id
  route_table_id = aws_route_table.private_rt.id
}

# ==============================================================================
# 5. SECURITY GROUPS
# ==============================================================================
# Security Group for EC2 (App Server)
resource "aws_security_group" "ec2_sg" {
  name        = "ec2-app-sg"
  description = "Allow HTTP/HTTPS and SSH access"
  vpc_id      = aws_vpc.main.id

  ingress {
    description = "SSH from anywhere (restrict to your IP in production)"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  # Flask Default Port
  ingress {
    description = "Flask Application Port"
    from_port   = 5000
    to_port     = 5000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  ingress {
    description = "HTTP Traffic"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    ="-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "ec2-security-group"
  }
}

# Security Group for RDS MySQL (Only accepts traffic from EC2)
resource "aws_security_group" "rds_sg" {
  name        = "rds-mysql-sg"
  description = "Allow MySQL traffic from EC2 instances"
  vpc_id      = aws_vpc.main.id

  ingress {
    description     = "MySQL port from EC2 Security Group"
    from_port       = 3306
    to_port         = 3306
    protocol        = "tcp"
    security_groups = [aws_security_group.ec2_sg.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    ="-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "rds-security-group"
  }
}

# ==============================================================================
# 6. EC2 INSTANCE (APP SERVER)
# ==============================================================================
# Get latest Amazon Linux 2023 AMI
#data "aws_ami" "amazon_linux_2023" {
#  most_recent = true
#  owners      = ["amazon"]

#  filter {
#    name   = "name"
#    values = ["al2023-ami-2023*-x86_64"]
#  }
#}
# OLD (Amazon Linux):
# data "aws_ami" "amazon_linux_2023" { ... }

# NEW (Ubuntu 24.04 LTS):
data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"] # Canonical's official AWS ID

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd-gp3/ubuntu-noble-24.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}
#resource "aws_instance" "app_server" {
#  ami                    = data.aws_ami.amazon_linux_2023.id
#  instance_type          = "t3.micro"
#  subnet_id              = aws_subnet.public_subnet.id
#  vpc_security_group_ids = [aws_security_group.ec2_sg.id]

  # Optional: Replace with your actual SSH Key Pair name if created in AWS Console
#  key_name = "first_key_pair" 
#  tags = {
#    Name = "app-server"
#  }
#}
resource "aws_instance" "app_server" {
  ami                    = data.aws_ami.ubuntu.id # Updated reference
  instance_type          = "t3.micro"
  subnet_id              = aws_subnet.public_subnet.id
  vpc_security_group_ids = [aws_security_group.ec2_sg.id]
  key_name = "first_key_pair"
  tags = {
    Name = "ubuntu-app-server"
  }
}
# ==============================================================================
# 7. RDS MYSQL DATABASE
# ==============================================================================
# DB Subnet Group linking the private subnets
resource "aws_db_subnet_group" "rds_subnet_group" {
  name        = "rds-private-subnet-group"
  subnet_ids  = [aws_subnet.private_subnet_1.id, aws_subnet.private_subnet_2.id]

  tags = {
    Name = "RDS DB Subnet Group"
  }
}

resource "aws_db_instance" "mysql_db" {
  allocated_storage      = 20
  max_allocated_storage  = 100
  db_name                = "myappdb"
  engine                 = "mysql"
  engine_version         = "8.0"
  instance_class         = "db.t3.micro" # Free Tier eligible
  username               = "admin"
  password               = var.db_password # Replace with secure password/variable
  parameter_group_name   = "default.mysql8.0"
  db_subnet_group_name   = aws_db_subnet_group.rds_subnet_group.name
  vpc_security_group_ids = [aws_security_group.rds_sg.id]
  publicly_accessible    = false
  skip_final_snapshot    = true

  tags = {
    Name = "rds-mysql-instance"
  }
}

# ==============================================================================
# 8. OUTPUTS
# ==============================================================================
output "ec2_public_ip" {
  description = "Public IP address of the App Server EC2 instance"
  value       = aws_instance.app_server.public_ip
}

output "rds_endpoint" {
  description = "Endpoint of the RDS MySQL instance"
  value       = aws_db_instance.mysql_db.endpoint
}
