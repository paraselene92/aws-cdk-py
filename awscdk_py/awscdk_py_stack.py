from aws_cdk import core
from aws_cdk import aws_ec2 as ec2
from awscdk_py.vars import var

class AwscdkPyStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        hensu = var()

        for subnetInfo in hensu.subnetInfoArray:
            subnetCfg = ec2.SubnetConfiguration(
                name = subnetInfo[0],
                subnet_type = subnetInfo[1],
                cidr_mask = subnetInfo[2]
            )
            hensu.subnetCfgArray.append(subnetCfg)

        myVPC = self.createVpc(
            hensu.vpcCidr, 
            hensu.vpcName, 
            hensu.enableDnsSupport, 
            hensu.maxAZs, 
            hensu.natGateways, 
            hensu.subnetCfgArray
        ) 

        mySecurityGroup = self.createSg(hensu.sgName, myVPC)
        for sgInfo in hensu.sgInfoArray:
            self.addSg(mySecurityGroup, sgInfo[0], sgInfo[1], sgInfo[2], sgInfo[3], sgInfo[4])
        
        # subnet を指定しないとデフォルトのサブネットにインスタンスを作成してしまうので指定の必要がある
        for public_subnet in myVPC.public_subnets:
            myPublicInstance = self.createInstance(
                id=hensu.PublicInstanceName, 
                image_id=hensu.PublicInstanceAmiId, 
                instance_type=ec2.InstanceType(hensu.PublicInstanceType).to_string(),
                subnet_id=public_subnet.subnet_id,
                security_group_ids=[mySecurityGroup.security_group_id],
            )
        
        # isolated には sg をかけないのでコメント扱い
        for isolated_subnet in myVPC.isolated_subnets:
            myIsolatedInstance = self.createInstance(
                id=hensu.IsolatedInstanceName, 
                image_id=hensu.IsolatedInstanceAmiId, 
                instance_type=ec2.InstanceType(hensu.IsolatedInstanceType).to_string(),
                subnet_id=isolated_subnet.subnet_id,
                #security_group_ids=[mySecurityGroup.security_group_id]
            )
        
        self.outputCfn("myPublicInstance_attr_public_ip", myPublicInstance.attr_public_ip)
        self.outputCfn("myPublicInstance_attr_private_ip", myPublicInstance.attr_private_ip)
        self.outputCfn("myIsolatedInstance_attr_private_ip", myIsolatedInstance.attr_private_ip)
        
    
    def addSg(self, sg, cidr, proto, string_representation, from_port, to_port):
        if (proto == "TCP"):
            protocol = ec2.Protocol.TCP
        elif (proto == "UDP"):
            protocol = ec2.Protocol.UDP
        elif (proto == "ICMP"):
            protocol = ec2.Protocol.ICMP
        sg.add_ingress_rule(
            peer=ec2.Peer.ipv4(cidr),
            connection=ec2.Port(
                protocol=protocol,
                string_representation=string_representation,
                from_port=from_port,
                to_port=to_port
            ) 
        )

    def createVpc(self, Cidr, Name, EDS, mAZs, natGWs, subnetCfg):
        vpc = ec2.Vpc(self, 
            Name, 
            cidr=Cidr, 
            enable_dns_support=EDS, 
            max_azs=mAZs, 
            nat_gateways=natGWs, 
            subnet_configuration=subnetCfg
        )
        return vpc

    def createSg(self, Name, vpc):
        sg = ec2.SecurityGroup(
            scope=self,
            id=Name,
            vpc=vpc
        )
        return sg

    def createInstance(self, id, image_id, instance_type, subnet_id, security_group_ids=[]):
        instance = ec2.CfnInstance(
            scope=self,
            id=id,
            image_id=image_id,
            instance_type=instance_type,
            subnet_id=subnet_id,
            security_group_ids=security_group_ids
        )
        return instance

    def outputCfn(self, id, variable):
        core.CfnOutput(
            scope=self,
            id=id,
            value=variable
        )

