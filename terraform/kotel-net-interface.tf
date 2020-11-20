resource "aws_network_interface" "kotelEth0" {
  subnet_id       = aws_subnet.kotelSubnet.id
  security_groups = [aws_security_group.KotelSG.id]
  
  tags = {
    Name          = "Kotel Network Interface"
  }
}