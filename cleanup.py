#!/usr/bin/env python

import argparse
from boto import ec2
import os
import pprint
import sys

def main(profile=None, region='us-west-2', del_flag=None):
    
    pp = pprint.PrettyPrinter(indent=4)

    conn = ec2.connect_to_region(region, profile_name=profile)
    
    allgroups = []
    # Get ALL security groups names
    groups = conn.get_all_security_groups()
    for groupobj in groups:
        allgroups.append(groupobj.name)
    
    # Get [running|stopped] instances security groups
    groups_in_use = []
    for state in ['running','stopped']:
        reservations = conn.get_all_instances(filters={'instance-state-name': state})
        for r in reservations:
            for inst in r.instances:
                if inst.groups[0].name not in groups_in_use:
                    groups_in_use.append(inst.groups[0].name)
    
    delete_candidates = []
    for group in allgroups:
        if group not in groups_in_use:
            delete_candidates.append(group)
    
    if del_flag == 'yes':
        print "We will now delete security groups identified to not be in use."
        for group in delete_candidates:
            print 'group for delete', group
            #conn.delete_security_group(group)
        print "We have deleted %d groups." % (len(delete_candidates))
        
        print "The list of security groups that are in use."
        pp.pprint(sorted(groups_in_use))
        print "Total of %d groups targeted for being in use." % (len(groups_in_use))        
        
    else:
        print "The list of security groups to be removed is below."
        print "Run this again with `--delete` to remove them"
        pp.pprint(sorted(delete_candidates))
        print "Total of %d groups targeted for removal." % (len(delete_candidates))
        
        print "The list of security groups that are in use."
        pp.pprint(sorted(groups_in_use))
        print "Total of %d groups targeted for being in use." % (len(groups_in_use))
    
if __name__ == '__main__': 
  
    parser = argparse.ArgumentParser()

    parser.add_argument('--profile', help='profile name in your ~/.boto config', required=True) 
    parser.add_argument('--delete', help='delete yes or no', required=True)
    parser.add_argument('--region', help='', required=True)

    args = parser.parse_args()
    
    main(profile=args.profile,  region=args.region, del_flag=args.delete)
