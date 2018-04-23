#!/bin/python

# To execute this sample program create a configuration file
# in json format as below and pass the path when asked
#
# 1. If certificate based authentication not applicable for etcd
# {
#     "integration_id": "uuid id of the cluster",
#     "etcd_host": "fqdn of the etcd host"
# }
#
# 2. If certificate based authentication is applicable for etcd
#
# {
#     "integration_id": "uuid id of the cluster",
#     "etcd_host": "fqdn of the etcd host",
#     "etcd_cert_file": "certificate file path",
#     "etcd_key_file": "certificate key file path",
#     "etcd_ca_cert_file": "ca certificate file path"
# }

import etcd
import json
import shutil
import sys


if __name__ == "__main__":
    print "\n==== BE WARNED THAT THIS WOULD REMOVE ALL THE CLUSTER DETAILS\n" \
        "==== FROM ETCD AND GRAPHITE. MAKE SURE YOU ARE PRETTY SURE ABOUT THIS\n" \
        "==== DELETION\n"
    print "==== ALSO MAKE SURE SERVICES collectd, tendrl-node-agent and \n" \
        "==== tendrl-gluster-integration ARE STOPPED ON ALL THE GLUSTER \n" \
        "==== STORAGE NODES\n"

    option = raw_input(" Do you want to continue (y/n) ? ")

    if option and option.lower() == 'y':
        conf_file_path = raw_input(" Enter the configuration file path: ")
        print ""
        cfgs = None
        with open(conf_file_path) as f:
            cont = f.read()
            cfgs = json.loads(cont)
        if cfgs:
            kwargs = {
                'host': cfgs['etcd_host'],
                'port': 2379
            }
            if 'etcd_cert_file' in cfgs:
                kwargs.update(
                    {
                        'ca_cert': cfgs['etcd_ca_cert_file'],
                        'cert': (cfgs['etcd_cert_file'], cfgs['etcd_key_file']),
                        'protocol': 'https'
                    }
                )
            client = etcd.Client(**kwargs)

            # Remove the etcd details for the cluster
            try:
                client.delete('/clusters/%s' % cfgs['integration_id'], recursive=True)
            except etcd.EtcdKeyNotFound:
                print "Cluster %s doesn't exist" % cfgs['integration_id']

            # Remove the graphite data for the cluster
            graphit_path = '/var/lib/carbon/whisper/tendrl/clusters/%s' % cfgs['integration_id']
            try:
                shutil.rmtree(graphit_path)
            except OSError:
                print "Dir/File %s doesn't exist" % graphit_path
    else:
        print " Ok. bye..."
