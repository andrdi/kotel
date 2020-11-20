resource "aws_vpc" "kotelVPC" {
  cidr_block = "192.168.0.0/24"

  tags = {
    Name = "Kotel VPC"
  }
}

resource "aws_internet_gateway" "KotelGW" {
  vpc_id = aws_vpc.kotelVPC.id

  tags = {
    Name = "Kotel GW"
  }
}

resource "aws_route_table" "kotelRouteTable" {
  vpc_id = aws_vpc.kotelVPC.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.KotelGW.id
  }

  tags = {
    Name = "Kotel Route Table"
  }
}