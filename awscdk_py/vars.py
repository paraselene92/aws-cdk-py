from aws_cdk import aws_ec2 as ec2
import requests

class var:

    # vars
    def __init__(self):

        # vpc
        self.vpcName = "testVpc"
        self.vpcCidr = "192.168.96.0/20"
        self.enableDnsSupport = True
        self.maxAZs = 1
        self.natGateways = 0
        self.sgCidr = "192.168.0.0/24"
        # instance
        self.PublicInstanceName = "softetherInstance"
        self.PublicInstanceAmiId = "ami-089fea7afa1321a09"
        self.PublicInstanceType = "t2.micro"
        self.IsolatedInstanceName = "IsolatedInstance"
        self.IsolatedInstanceAmiId = "ami-0b69ea66ff7391e80" # AmazonLinux2
        self.IsolatedInstanceType = "t2.micro"
        # subnet
        self.subnetCfgArray = []
        self.subnetInfoArray = [
            ("publicSubnet", ec2.SubnetType.PUBLIC, 24),
            ("isolatedSubnet", ec2.SubnetType.ISOLATED, 24)
        ]
        # sg
        self.sgName = "mysg"
        self.sgInfoArray = [
            (self.sgCidr, "TCP", "", 22, 22),
            (self.sgCidr, "ICMP", "vpc", -1, -1),
            (self.getMyIp()+"/32", "TCP", "vpc", 22, 22),
            (self.getMyIp()+"/32", "UDP", "vpc2", 500, 500),
            (self.getMyIp()+"/32", "UDP", "vpc3", 4500, 4500)
        ]

    def getMyIp(self):
        res = requests.get("http://inet-ip.info/ip")
        return res.text