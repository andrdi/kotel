resource "aws_eip" "kotelServerEIP" {
  network_interface = aws_network_interface.kotelEth0.id
  vpc               = true
}