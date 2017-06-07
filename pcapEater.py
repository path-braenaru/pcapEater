#!/usr/bin/env python2


import argparse
import dpkt
import os


class co:
    DCY = '\033[36m'
    G = '\033[92m'
    R = '\033[91m'
    B = '\033[1m'
    E = '\033[0m'


def crunch(GET_reqList, POST_reqList, outfile):
    if len(GET_reqList) > 0:
        print(
            co.G +
            '\n[+] GET Requests found! (de-duplicated output)\n' +
            co.E
        )
        with open(outfile, 'w+') as ofile:
            for i in GET_reqList:
                print(
                    co.B +
                    i + '\n' +
                    co.E
                )
                ofile.write(
                    i +
                    '\n'
                )
            ofile.close()
        print(
            co.G +
            '\n[+] GET Request URIs written to %s' % outfile +
            co.E
        )
    else:
        print(
            co.R +
            '\n[-] No GET Requests found!\n' + 
            co.E
        )
    if len(POST_reqList) > 0:
        print(
            co.DCY +
            '\n[+] POST Requests found! (de-duplicated output)\n' +
            co.E
        )
        for x in POST_reqList:
            print(
                co.B +
                x +
                co.E
            )
        print(
            co.DCY +
            '\n[-] POST Requests not written to file\n' +
            co.E 
        )
    else:
        print(
            co.R +
            '\n[-] No POST Requests found!\n' +
            co.E
        )
        exit(0)


def pcapEater(infile, httpPorts):
    GET_reqList = []
    GET_staging = []
    POST_reqList = []
    POST_staging = []

    with open(infile, 'r') as incap:
        pcap = dpkt.pcap.Reader(incap)
        for timestamp, buf in pcap:
            try:
                ethernet = dpkt.ethernet.Ethernet(buf)
                ip = ethernet.data
                tcp = ip.data
                if tcp.__class__.__name__ == 'TCP':
                    if tcp.dport in httpPorts:
                        if len(tcp.data) > 0:
                            try:
                                http = dpkt.http.Request(tcp.data)
                                if http.method == 'GET':
                                    GET_staging.append(
                                        http.headers['host'] +
                                        http.uri
                                    )
                                elif http.method == 'POST':
                                    POST_staging.append(
                                        http.headers['host'] +
                                        http.uri
                                    )
                            except Exception, e:
                                pass
            except:
                pass
        incap.close()

    for a in GET_staging:
        if a not in GET_reqList:
            GET_reqList.append(a)
    for b in POST_staging:
        if b not in POST_reqList:
            POST_reqList.append(b)

    return GET_reqList, POST_reqList


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument(
        '-i',
        '--infile'
    )
    p.add_argument(
        '-o',
        '--outfile'
    )
    p.add_argument(
        '-p',
        '--ports'
    )
    args = p.parse_args()
    infile = args.infile
    outfile = args.outfile
    ports = args.ports
    if not infile:
        print(
            co.B +\
            '\nNeed an input pcap!\nUse pcapEater.py -i input-file.pcap\n' +\
            co.E
        )
        exit(0)
    if not os.path.exists('./outputs/'):
        os.makedirs('./outputs/')
    if not outfile:
        print('\n[-] No output file specified! saving to ./outputs/output.%s.txt\n' % infile)
        outfile = './outputs/output.%s.txt' % infile
    if not ports:
        print('[-] No ports specified! Defaulting to 80, 8080')
        httpPorts = [
            80,
            8080
        ]
    else:
        httpPorts = []
        ports = str(ports).split(',')
        for port in ports:
            httpPorts.append(int(port))
        print('Ports specified : %s' % httpPorts)
    GET_reqList, POST_reqList = pcapEater(infile, httpPorts)
    crunch(
        GET_reqList,
        POST_reqList,
        outfile
    )
