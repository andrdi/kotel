resource "aws_security_group" "KotelSG" {
  name        = "KotelSG"
  description = "Allow SSH traffic"
  vpc_id      = aws_vpc.kotelVPC.id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port       = 0
    to_port         = 0
    protocol        = "-1"
    cidr_blocks     = ["0.0.0.0/0"]
  }

  tags = {
    Name = "allow_ssh"
  }
}