resource "aws_subnet" "kotelSubnet" {
  vpc_id     = aws_vpc.kotelVPC.id
  cidr_block = "192.168.0.0/24"
  map_public_ip_on_launch = true

  tags = {
    Name = "Kotel Subnet"
  }
}

resource "aws_route_table_association" "a" {
  subnet_id      = aws_subnet.kotelSubnet.id
  route_table_id = aws_route_table.kotelRouteTable.id
}