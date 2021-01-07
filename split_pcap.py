#!/usr/local/bin/python2.7

import dpkt

#for statistic
counter=0
ipcounter=0
tcpcounter=0
udpcounter=0
icmpcounter=0

filename='test.pcap'
pcap_all = dpkt.pcap.Reader(open(filename,'r'))
for ts, pkt in pcap_all:

    counter+=1
    eth=dpkt.ethernet.Ethernet(pkt) 
    if eth.type!=dpkt.ethernet.ETH_TYPE_IP:
       continue

    ip=eth.data
    ipcounter+=1

    if ip.p==dpkt.ip.IP_PROTO_TCP: 
       tcpcounter+=1

    if ip.p==dpkt.ip.IP_PROTO_UDP:
       udpcounter+=1

    if ip.p==dpkt.ip.IP_PROTO_ICMP:
       icmpcounter+=1
print "Total number of packets in the pcap file: ", counter
print "Total number of ip packets: ", ipcounter
print "Total number of tcp packets: ", tcpcounter
print "Total number of udp packets: ", udpcounter
print "Total number of icmp packets: ", icmpcounter

#split pcap file
ratio=0.7
remain= 1 - ratio
outfile_name1 = filename + str(ratio)
outfile_name2 = filename + str(remain)
# Open a file for writing packets
outfile1 = open(outfile_name1, "w")
outfile2 = open(outfile_name2, "w")

writer1 = dpkt.pcap.Writer(outfile1)
writer2 = dpkt.pcap.Writer(outfile2)

temp_count=0
for ts, pkt in pcap_all:
	if temp_count < counter*ratio:
		writer1.writepkt(pkt)
		outfile1.flush()
	else:
		writer2.writepkt(pkt)
		outfile2.flush()
	temp_count += 1		

# closing file
outfile1.close()
outfile2.close()

print "AND WE DONE :D"
