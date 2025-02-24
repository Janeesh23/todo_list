resource "aws_instance" "jenkins" {
  ami                    = data.aws_ami.amiID_for_ubuntu.id
  instance_type          = "t3.small"
  key_name               = "cicdkey"
  vpc_security_group_ids = [aws_security_group.jenkins-sg.id]


  tags = {
    Name = "jenkins-master-server"
  }
}
resource "aws_ec2_instance_state" "jenkins_state" {
  instance_id = aws_instance.jenkins.id
  state       = "stopped"
}

resource "aws_instance" "control" {
  ami                    = data.aws_ami.amiID_for_ubuntu.id
  instance_type          = "t3.micro"
  key_name               = "cicdkey"
  vpc_security_group_ids = [aws_security_group.control-sg.id]


  tags = {
    Name = "control-server"
  }
}
resource "aws_ec2_instance_state" "control_state" {
  instance_id = aws_instance.control.id
  state       = "running"
}