data "aws_ami" "amiID_for_ubuntu" {
  most_recent = true
  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]

  }
  owners = ["099720109477"]

}

output "instance_id" {
  description = "ami id of the instance"
  value       = data.aws_ami.amiID_for_ubuntu

}
