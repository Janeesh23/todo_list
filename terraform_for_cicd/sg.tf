data "http" "my_ip" {
  url = "https://checkip.amazonaws.com"
}

# jenkins-server-security-group
resource "aws_security_group" "jenkins-sg" {
  name        = "jenkins-sg"
  description = "Security group for Jenkins instance"


  tags = {
    Name = "for-jenkins"
  }
}

resource "aws_vpc_security_group_ingress_rule" "allow_ssh_from_my_ip_jenkins" {
  security_group_id = aws_security_group.jenkins-sg.id
  cidr_ipv4         = "${trimspace(data.http.my_ip.response_body)}/32"
  from_port         = 22
  ip_protocol       = "tcp"
  to_port           = 22
}

resource "aws_vpc_security_group_ingress_rule" "allow_frontend_from_my_ip_jenkins" {
  security_group_id = aws_security_group.jenkins-sg.id
  cidr_ipv4         = "${trimspace(data.http.my_ip.response_body)}/32"
  from_port         = 8080
  ip_protocol       = "tcp"
  to_port           = 8080
}

resource "aws_security_group_rule" "allow_control_to_jenkins_sg" {
  type                     = "ingress"
  from_port                = 22
  to_port                  = 22
  protocol                 = "tcp"
  security_group_id        = aws_security_group.jenkins-sg.id
  source_security_group_id = aws_security_group.control-sg.id
}

resource "aws_vpc_security_group_egress_rule" "allow_all_traffic_ipv4_jenkins" {
  security_group_id = aws_security_group.jenkins-sg.id
  cidr_ipv4         = "0.0.0.0/0"
  ip_protocol       = "-1"
}


# control-machine-security-group
resource "aws_security_group" "control-sg" {
  name        = "control-sg"
  description = "Security group for control instance"


  tags = {
    Name = "for-control"
  }
}

resource "aws_vpc_security_group_ingress_rule" "allow_ssh_from_my_ip_to_control" {
  security_group_id = aws_security_group.control-sg.id
  cidr_ipv4         = "${trimspace(data.http.my_ip.response_body)}/32"
  from_port         = 22
  ip_protocol       = "tcp"
  to_port           = 22
}

resource "aws_vpc_security_group_egress_rule" "allow_all_traffic_ipv4_control" {
  security_group_id = aws_security_group.control-sg.id
  cidr_ipv4         = "0.0.0.0/0"
  ip_protocol       = "-1"
}

