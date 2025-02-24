import json
import os
import pathlib
import random
import sys
import ipaddress
import copy
from typing import TypedDict


class SecurityGroupEntry(TypedDict):
    GroupId: str
    GroupName: str


class TagEntry(TypedDict):
    Key: str
    Value: str


def generate_random_id(prefix, length=17) -> str:
    """Generates a random ID string with the given prefix."""
    chars = "abcdef0123456789"
    random_part = "".join(random.choice(chars) for _ in range(length))
    return f"{prefix}-{random_part}"


def generate_mac_address() -> str:
    """Generates a random MAC address."""
    return "02:" + ":".join(f"{random.randint(0, 255):02x}" for _ in range(5))


def create_security_group_entry(vpc_id: str, owner_id: str) -> tuple[list[SecurityGroupEntry], dict]:
    """Generates a random security group ID, name, and definition."""
    group_id = generate_random_id("sg")
    group_name = f"sg-{random.randint(1000, 9999)}"

    security_group_definition: dict = {
        "Description": f"Security group {group_name}",
        "GroupId": group_id,
        "GroupName": group_name,
        "IpPermissions": [
            {
                "FromPort": 22,  # Allow SSH
                "IpProtocol": "tcp",
                "IpRanges": [{"CidrIp": "0.0.0.0/0"}],
                "Ipv6Ranges": [],
                "PrefixListIds": [],
                "ToPort": 22,
                "UserIdGroupPairs": [],
            }
        ],
        "IpPermissionsEgress": [
            {
                "IpProtocol": "-1",  # Allow all outbound traffic
                "IpRanges": [{"CidrIp": "0.0.0.0/0"}],
                "Ipv6Ranges": [],
                "PrefixListIds": [],
                "UserIdGroupPairs": [],
            }
        ],
        "OwnerId": owner_id,
        "SecurityGroupArn": f"arn:aws:ec2:us-west-2:{owner_id}:security-group/{group_id}",
        "Tags": [{"Key": "Name", "Value": group_name}],
        "VpcId": vpc_id,
    }
    return [{"GroupId": group_id, "GroupName": group_name}], security_group_definition


def create_ec2_instance_entry(instance_num: int, 
                              ip_address: ipaddress.IPv4Address, 
                              eni_id: str, 
                              eni_attachment_id: str, 
                              security_groups: list[SecurityGroupEntry], 
                              tags: list[TagEntry],
                              vpc_id: str,
                              subnet_id: str,
                              availability_zone: str) -> dict:
    """Creates a single EC2 instance entry for Reservations.json with a configurable availability zone."""
    instance_id = generate_random_id("i")
    volume_id = generate_random_id("vol")
    mac_address = generate_mac_address()
    client_token = generate_random_id("terraform")
    interface = create_network_interface_entry(
        instance_id=instance_id,
        ip_address=ip_address,
        eni_id=eni_id,
        eni_attach_id=eni_attachment_id,
        mac_address=mac_address,
        security_groups=security_groups,
        tags=tags,
        vpc_id=vpc_id,
        subnet_id=subnet_id,
        availability_zone=availability_zone)
    # Derive region from availability_zone (e.g., 'us-west-2a' -> 'us-west-2')
    region = get_region_from_az(availability_zone)
    private_dns = make_dns_name(ip_address, region)

    instance_data: dict = {
        "AmiLaunchIndex": 0,
        "Architecture": "x86_64",
        "BlockDeviceMappings": [
            {
                "DeviceName": "/dev/xvda",
                "Ebs": {
                    "AttachTime": "2025-01-16 22:12:19+00:00",
                    "DeleteOnTermination": True,
                    "Status": "attached",
                    "VolumeId": volume_id,
                },
            }
        ],
        "BootMode": "uefi-preferred",
        "CapacityReservationSpecification": {"CapacityReservationPreference": "open"},
        "ClientToken": client_token,
        "CpuOptions": {"CoreCount": 1, "ThreadsPerCore": 1},
        "CurrentInstanceBootMode": "legacy-bios",
        "EbsOptimized": False,
        "EnaSupport": True,
        "EnclaveOptions": {"Enabled": False},
        "HibernationOptions": {"Configured": False},
        "Hypervisor": "xen",
        "ImageId": "ami-0b4a21432a0c9c1ab",
        "InstanceId": instance_id,
        "InstanceType": "t2.micro",
        "KeyName": "sshkey_20240103",
        "LaunchTime": "2025-01-16 22:12:18+00:00",
        "MaintenanceOptions": {"AutoRecovery": "default"},
        "MetadataOptions": {
            "HttpEndpoint": "enabled",
            "HttpProtocolIpv6": "disabled",
            "HttpPutResponseHopLimit": 2,
            "HttpTokens": "required",
            "InstanceMetadataTags": "disabled",
            "State": "applied",
        },
        "Monitoring": {"State": "disabled"},
        "NetworkInterfaces": [interface],
        #     {
        #         "Attachment": {
        #             "AttachTime": "2025-01-16 22:12:18+00:00",
        #             "AttachmentId": eni_attachment_id,
        #             "DeleteOnTermination": True,
        #             "DeviceIndex": 0,
        #             "NetworkCardIndex": 0,
        #             "Status": "attached",
        #         },
        #         "Description": "",
        #         "Groups": security_groups,
        #         "InterfaceType": "interface",
        #         "Ipv6Addresses": [],
        #         "MacAddress": mac_address,
        #         "NetworkInterfaceId": eni_id,
        #         "Operator": {"Managed": False},
        #         "OwnerId": "310950261294",
        #         "PrivateDnsName": private_dns,
        #         "PrivateIpAddress": str(ip_address),
        #         "PrivateIpAddresses": [
        #             {
        #                 "Primary": True,
        #                 "PrivateDnsName": private_dns,
        #                 "PrivateIpAddress": str(ip_address),
        #             }
        #         ],
        #         "SourceDestCheck": True,
        #         "Status": "in-use",
        #         "SubnetId": subnet_id,
        #         "VpcId": vpc_id,
        #     }
        # ],
        "NetworkPerformanceOptions": {"BandwidthWeighting": "default"},
        "Operator": {"Managed": False},
        "Placement": {
            "AvailabilityZone": availability_zone,
            "GroupName": "",
            "Tenancy": "default",
        },
        "PlatformDetails": "Linux/UNIX",
        "PrivateDnsName": private_dns,
        "PrivateDnsNameOptions": {
            "EnableResourceNameDnsAAAARecord": False,
            "EnableResourceNameDnsARecord": False,
            "HostnameType": "ip-name",
        },
        "PrivateIpAddress": str(ip_address),
        "ProductCodes": [],
        "PublicDnsName": "ec2-35-86-161-173.us-west-2.compute.amazonaws.com",
        "PublicIpAddress": "35.86.161.173",
        "RootDeviceName": "/dev/xvda",
        "RootDeviceType": "ebs",
        "SecurityGroups": security_groups,
        "SourceDestCheck": True,
        "State": {"Code": 16, "Name": "running"},
        "StateTransitionReason": "",
        "SubnetId": subnet_id,
        "Tags": tags,
        "UsageOperation": "RunInstances",
        "UsageOperationUpdateTime": "2025-01-16 22:12:18+00:00",
        "VirtualizationType": "hvm",
        "VpcId": vpc_id,
    }

    return instance_data

def make_dns_name(ip_address, region):
    return f"ip-{str(ip_address).replace('.', '-')}.{region}.compute.internal"

def get_region_from_az(availability_zone):
    return availability_zone[:-1] if availability_zone[-1].isalpha() else availability_zone


def create_network_interface_entry(
    instance_id: str,
    ip_address: ipaddress.IPv4Address,
    eni_id: str,
    eni_attach_id: str,
    mac_address: str,
    security_groups: list[SecurityGroupEntry],
    tags: list[TagEntry],
    vpc_id: str,
    subnet_id: str,
    availability_zone: str
) -> dict:
    """Creates a single network interface entry for NetworkInterfaces.json, with configurable tags and dynamic VPC, subnet, and AZ."""
    return {
        "Attachment": {
            "AttachTime": "2024-07-26T12:00:00+00:00",
            "AttachmentId": eni_attach_id,
            "DeleteOnTermination": True,
            "DeviceIndex": 0,
            "InstanceId": instance_id,
            "InstanceOwnerId": "554773406868",
            "Status": "attached",
        },
        "AvailabilityZone": availability_zone,
        "Description": "Primary network interface",
        "Groups": security_groups,
        "InterfaceType": "interface",
        "Ipv6Addresses": [],
        "MacAddress": mac_address,
        "NetworkInterfaceId": eni_id,
        "OwnerId": "554773406868",
        "PrivateIpAddress": str(ip_address),
        "PrivateIpAddresses": [
            {
                "Primary": True,
                "PrivateIpAddress": str(ip_address),
            }
        ],
        "RequesterManaged": False,
        "SourceDestCheck": True,
        "Status": "in-use",
        "SubnetId": subnet_id,
        "TagSet": tags,
        "VpcId": vpc_id,
    }


def create_reservation_entry(instances):
    """Creates a single reservation entry for Reservations.json."""
    reservation_id = generate_random_id("r")
    return {
        "Groups": [],
        "Instances": instances,
        "OwnerId": "554773406868",
        "ReservationId": reservation_id,
    }


def load_existing_data(filename):
    """Loads existing data from a JSON file."""
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        if "Reservations" in filename:
            return {"Reservations": []}
        elif "NetworkInterfaces" in filename:
            return {"NetworkInterfaces": []}
        elif "SecurityGroups" in filename:
            return {"SecurityGroups": []}
        return {}


def generate_aws_json(
        aws_configs_dir: os.PathLike,
        num_instances: int,
        start_ip: ipaddress.IPv4Address = None):
    """
    Generates and returns AWS configuration data for EC2 instances, network interfaces, and security groups in JSON format.

    This function loads existing configuration JSON files from the specified directory, and then creates entries for a given number of EC2 instances.
    For each instance, a network interface entry is created along with a corresponding security group (rotating every three instances). The function also
    handles assigning IP addresses, tags, and generating identifiers and MAC addresses.

    Parameters:
        aws_configs_dir (os.PathLike): The directory containing the AWS configuration JSON files ("Reservations.json", "NetworkInterfaces.json", and "SecurityGroups.json").
        num_instances (int): The number of EC2 instances to generate.
        start_ip (ipaddress.IPv4Address, optional): The starting IP address for the generated instances. If None, defaults to "10.30.1.4" or the next available IP based on existing data.

    Returns:
        tuple: A tuple containing three elements:
            - reservations_data (dict): Updated JSON data representing EC2 instance reservations.
            - network_interfaces_data (dict): Updated JSON data for network interfaces.
            - security_groups_data (dict): Updated JSON data for security groups.

    Raises:
        ValueError: If the provided aws_configs_dir is not a directory.
    """
    # Check if pathlib.Path(aws_configs_dir) is a directory
    if not pathlib.Path(aws_configs_dir).is_dir():
        raise ValueError(f"{aws_configs_dir} is not a directory")
    reservations_data = load_existing_data(pathlib.Path(aws_configs_dir) / "Reservations.json")
    network_interfaces_data = load_existing_data(pathlib.Path(aws_configs_dir) / "NetworkInterfaces.json")
    security_groups_data = load_existing_data(pathlib.Path(aws_configs_dir) / "SecurityGroups.json")

    vpc_id = generate_random_id('vpc')
    owner_id = "310950261294"
    subnet_id = generate_random_id('subnet')
    availability_zone = "us-west-2a"

    if security_groups_data["SecurityGroups"]:
        try:
            vpc_id = security_groups_data["SecurityGroups"][0]["VpcId"]
            owner_id = security_groups_data["SecurityGroups"][0]["OwnerId"]
        except KeyError:
            pass # Stick with the default values

    # Pull the subnet_id from the first EC2 instance
    if reservations_data["Reservations"]:
        try:
            subnet_id = reservations_data["Reservations"][0]["Instances"][0]["NetworkInterfaces"][0]["SubnetId"]
            availability_zone = reservations_data["Reservations"][0]["Instances"][0]["Placement"]["AvailabilityZone"]
        except KeyError:
            pass # Stick with the default values

    if start_ip is None:
        start_ip = ipaddress.ip_address("10.30.1.4")
    if reservations_data["Reservations"]:
        existing_ips = [
            ipaddress.ip_address(interface["PrivateIpAddress"])
            for reservation in reservations_data["Reservations"]
            for instance in reservation["Instances"]
            for interface in instance["NetworkInterfaces"]
        ]
        if existing_ips:
            start_ip = max(existing_ips) + 1
    else:
        reservations_data["Reservations"] = []

    EC2_PER_SG = 3
    security_groups = None  # Initialize outside the loop
    security_group_definition = None
    sg_instance_count = 0  # Counter for instances using the current SG
    instances = []
    for i in range(num_instances):
        ip_address = start_ip + i
        eni_id = generate_random_id("eni")
        eni_attach_id = generate_random_id("eni-attach")
        mac_address = generate_mac_address()

        # Generate a new security group every EC2_PER_SG instances
        if sg_instance_count % EC2_PER_SG == 0:
            security_groups, security_group_definition = create_security_group_entry(vpc_id, owner_id)
            security_groups_data["SecurityGroups"].append(security_group_definition)

        # Define tags, cycling through application_id 1, 2, and 3
        app_id = (sg_instance_count % EC2_PER_SG) + 1
        tags: list[TagEntry] = [
            {"Key": "Name", "Value": f"Instance-{i}"},
            {"Key": "application_id", "Value": str(app_id)},
        ]

        instance_entry = create_ec2_instance_entry(
            instance_num=i,
            ip_address=ip_address,
            eni_id=eni_id,
            eni_attachment_id=eni_attach_id,
            security_groups=security_groups,
            tags=tags,
            vpc_id=vpc_id,
            subnet_id=subnet_id,
            availability_zone=availability_zone
        )
        instances.append(instance_entry)

        instance_id = instance_entry["InstanceId"]
        network_interface_entry = create_network_interface_entry(
            instance_id=instance_id,
            ip_address=ip_address,
            eni_id=eni_id,
            eni_attach_id=eni_attach_id,
            mac_address=mac_address,
            security_groups=security_groups,
            tags=tags,
            vpc_id=vpc_id,
            subnet_id=subnet_id,
            availability_zone=availability_zone
        )
        network_interfaces_data["NetworkInterfaces"].append(network_interface_entry)

        sg_instance_count += 1  # Increment the counter

    reservations_data["Reservations"].append(create_reservation_entry(instances))

    return reservations_data, network_interfaces_data, security_groups_data


def main():
    """Generates EC2, Network Interface, and Security Group JSON data."""
    if len(sys.argv) != 2:
        print("Usage: python generate_ec2_json.py <number_of_instances>")
        sys.exit(1)

    try:
        num_instances = int(sys.argv[1])
    except ValueError:
        print("Error: Invalid number of instances.")
        sys.exit(1)

    reservations_data, network_interfaces_data, security_groups_data = generate_aws_json(pathlib.Path('.'), num_instances)

    with open("Reservations.json", "w") as f:
        json.dump(reservations_data, f, indent=1)
    with open("NetworkInterfaces.json", "w") as f:
        json.dump(network_interfaces_data, f, indent=1)
    with open("SecurityGroups.json", "w") as f:
        json.dump(security_groups_data, f, indent=1)

    print(f"Successfully generated data for {num_instances} instances.")
    print("Files created: Reservations.json, NetworkInterfaces.json, SecurityGroups.json")


if __name__ == "__main__":
    main()
