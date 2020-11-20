resource "aws_instance" "kotelServer" {
  ami           = "ami-0502e817a62226e03"
  instance_type = "t2.micro"
  key_name      = "kotel"
  root_block_device {
    volume_size = "25"
  }

  network_interface {
    network_interface_id = aws_network_interface.kotelEth0.id
    device_index         = 0
  }
  
  tags = {
    Name = "Kotel Server"
  }
}