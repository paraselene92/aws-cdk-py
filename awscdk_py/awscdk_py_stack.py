from aws_cdk import core
from aws_cdk import aws_ec2 as ec2

class AwscdkPyStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # The code that defines your stack goes here

        # Subnet
        subnetCfg = [
            {
                "name": "privateSubnet",
                "subnetType": ec2.SubnetType.ISOLATED,
                "cidrMask": 24,
            },
            {
                "name": "publicSubnet",
                "subnetType": ec2.SubnetType.PUBLIC,
                "cidrMask": 24,
            },
        ]

        # VPC_vars
        vpcName = "testVpc"
        vpcCidr = "192.168.0.0/20"
        enableDnsSupport = True
        maxAZs = 1
        natGateways = 0
        sgCidr = "192.168.0.0/24"

        myVPC = self.createVpc(vpcCidr, vpcName, enableDnsSupport, maxAZs, natGateways, subnetCfg) 

        mySecurityGroup = self.createSg("mysg", myVPC)
        mySecurityGroup.add_ingress_rule(
            peer=ec2.Peer.ipv4(sgCidr), 
            connection=ec2.Port(
                protocol=ec2.Protocol.TCP, 
                string_representation="vpc", 
                from_port=22,
                to_port=22
            )
        )
        
        # subnet を指定しないとデフォルトのサブネットにインスタンスを作成してしまうので指定の必要がある
        for isolated_subnet in myVPC.isolated_subnets:
            self.createInstance(
                id="aaa", 
                image_id="ami-089fea7afa1321a09", 
                instance_type=ec2.InstanceType("t2.micro").to_string(),
                security_group_ids=[mySecurityGroup.security_group_id], 
                subnet_id=isolated_subnet.subnet_id
            )

    def createVpc(self, Cidr, Name, EDS, mAZs, natGWs, subnetCfg):
        vpc = ec2.Vpc(self, Name, cidr=Cidr, enable_dns_support=EDS, max_azs=mAZs, nat_gateways=natGWs, subnet_configuration=subnetCfg)
        return vpc

    def createSg(self, Name, vpc):
        sg = ec2.SecurityGroup(
                scope=self,
                id=Name,
                vpc=vpc
        )
        return sg

    def createInstance(self, id, image_id, instance_type, security_group_ids, subnet_id):
        ec2.CfnInstance(
                scope=self,
                id=id,
                image_id=image_id,
                instance_type=instance_type,
                security_group_ids=security_group_ids,
                subnet_id=subnet_id
        )

    def outputCfn(self, idd, variable):
        core.CfnOutput(
                scope=self,
                id=idd,
                value=variable
        )

