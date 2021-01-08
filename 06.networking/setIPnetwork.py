import wmi

# Obtain network adaptors configurations
nic_configs = wmi.WMI().Win32_NetworkAdapterConfiguration(IPEnabled=True)

print (nic_configs)

# First network adaptor
nic = nic_configs[0]

print ("----Plese choose the option ----")
print ("-----press [0] for DHCP")
print ("-----press [1] for Static IP [172.28.25.200]")
value = input()
print ("your input", value)

if value == '0':
    # Enable DHCP
    nic.EnableDHCP()
    print ("Enable DHCP")
elif value == '1':
    # IP address, subnetmask and gateway values should be unicode objects
    ip = u'172.28.25.200'
    subnetmask = u'255.255.255.0'
    gateway = u'172.28.25.1'
    # Set IP address, subnetmask and default gateway
    # Note: EnableStatic() and SetGateways() methods require *lists* of values to be passed
    nic.EnableStatic(IPAddress=[ip],SubnetMask=[subnetmask])
    nic.SetGateways(DefaultIPGateway=[gateway])
    print ("Set Static IP address: ", ip)
else:
    print ("No thing changes")