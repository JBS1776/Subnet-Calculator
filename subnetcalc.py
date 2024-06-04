import re

maxip = 0xffffffff

# Main function checks for input correctness so that helper functions can assume correct input is inserted

def validip(ip):
    if ip.count('.') != 3:
        return False
    ipstr = ip.split('.')
    for i in range(0, 4):
        if not ipstr[i].isdigit():
            return False
        if int(ipstr[i]) >> 8 > 0:
            return False
    return True

def validsubnet(subnet):
    if isinstance(subnet, int):
        return subnet >= 0 and subnet <= 32
    else:
        # Subnets that are not powers of 2 are invalid
        ipnum = iptohex(subnet)
        sigbit = 1
        toshift = 31
        if ipnum == 0 or ipnum == maxip:
            return True
        while toshift > 0:
            tocmp = (sigbit << toshift) & maxip
            if tocmp > ipnum:
                return False
            if tocmp == ipnum:
                return True
            sigbit += (1 << (32 - toshift))
            toshift -= 1
        return False

def iptohex(ip):
    ipstr = ip.split('.')
    sl = 24
    hexvalue = 0
    for i in range(0, 4):
        hexvalue += int(ipstr[i]) << sl
        sl -= 8
    return hexvalue

def hextoip(val):
    result = ""
    sr = 24
    for i in range(0, 4):
        toadd = (val >> sr) & 0xff
        if i < 3:
            result += str(toadd) + "."
        else:
            result += str(toadd)
        sr -= 8
    return result

def cidrtosubnet(subnet):
    sl = 32 - subnet
    return maxip & (maxip << sl)

def subnettoip(subnet):
    return hextoip(cidrtosubnet(subnet))

def subnetiptocidr(ip):
    subnetip = iptohex(ip)
    if subnetip == 0:
        return 0
    sigbit = 1
    toshift = 31
    while toshift > 0:
        tocmp = (sigbit << toshift) & maxip
        if tocmp == subnetip:
            return 32 - toshift
        sigbit += (1 << (32 - toshift))
        toshift -= 1
    return 32

def cidrtowildcard(subnet):
    return ~(cidrtosubnet(subnet))

def wildcardtoip(subnet):
    return hextoip(cidrtowildcard(subnet))

def totalhostcount(subnet):
    return (cidrtowildcard(subnet) + 1) & maxip

def usablehostcount(subnet):
    if subnet == 31 or subnet == 32:
        return 32 - subnet
    return (totalhostcount(subnet) - 2) & maxip

def networkaddr(ip, subnet):
    return iptohex(ip) & cidrtosubnet(subnet)

def bcastaddr(ip, subnet):
    return iptohex(ip) | cidrtowildcard(subnet)

def listsubnetsperhost(ip, insubnet):
    count = 1
    subnet = 0
    if not isinstance(insubnet, int):
        subnet = subnetiptocidr(insubnet)
    else:
        subnet = insubnet
    while subnet <= 32:
        startaddress = networkaddr(ip, subnet)
        endaddress = bcastaddr(ip, subnet)
        print("Subnet " + str(subnet) + ": " + hextoip(cidrtosubnet(subnet))
             + " First network: " + hextoip(startaddress) 
              + " - " + hextoip(endaddress) + " Subnet count: " + str(count)
              + " Usable hosts per subnet: " + str(usablehostcount(subnet)))
        count <<= 1
        subnet += 1


def main():
    print('Give IP address')
    s = input()
    if not validip(s):
        print("IP is invalid!")
        return 1
    print('Give Subnet Mask')
    t = input()
    if t.isdigit():
        t = int(t)
    else:
        if not validip(t):
            print("Subnet is invalid!")
            return 1
    if not validsubnet(t):
        print("Subnet is invalid!")
        return 1
    listsubnetsperhost(s, t)

if __name__ == "__main__":
    main()
