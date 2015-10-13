#!/usr/bin/env python
import sys
from boto import ec2
import os
import argparse

#====================================================================
def main(profile=None, region='us-west-2', env='dev', ingress='yes', egress='no'):

    if profile is None:
        print 'You must pass profile argument to main function' 
        sys.exit()
    #create output directory
    try:
        os.makedirs('groups/'+env)
    except Exception as e:
        print '%s directory exist, moving on...' %env     
    print 'Looking up your dirty little secrets..'   
    conn = ec2.connect_to_region(region, profile_name=profile)
    security_group_dict = {}
    security_groups = conn.get_all_security_groups()

    for group in security_groups:
        sec_rules = group.rules
        sec_rules_egress = group.rules_egress
        group_name = group.name
        group_rules = {}
        group_rules_egress = {}
        
        for rule in sec_rules:
            if 'sg' in str(rule.grants):
                grant_name = str(rule.grants).split('-')[0]+'-'+str(rule.grants).split('-')[1]
                grant_name = grant_name.replace('[','')
                security_group = conn.get_all_security_groups(group_ids=grant_name)
                grant_sg_name = security_group[0].name
                group_rules[grant_sg_name] = {'cidr':grant_sg_name, 'to_port':rule.to_port, 'from_port':rule.from_port, 'type':'ingress', 'protocol': rule.ip_protocol}
            else:
                group_rules[str(rule.grants)] = {'cidr':str(rule.grants), 'to_port':rule.to_port, 'from_port':rule.from_port, 'type':'ingress', 'protocol': rule.ip_protocol}

        for rule in sec_rules_egress:
            if 'sg' in str(rule.grants):
                grant_name = str(rule.grants).split('-')[0]+'-'+str(rule.grants).split('-')[1]
                grant_name = grant_name.replace('[','')
                security_group = conn.get_all_security_groups(group_ids=grant_name)
                grant_sg_name = security_group[0].name
                group_rules_egress[grant_sg_name] = {'cidr':grant_sg_name, 'to_port':rule.to_port, 'from_port':rule.from_port, 'type':'egress', 'protocol': rule.ip_protocol}
            else:
                group_rules_egress[str(rule.grants)] = {'cidr':str(rule.grants), 'to_port':rule.to_port, 'from_port':rule.from_port, 'type':'egress', 'protocol': rule.ip_protocol}            
                
        security_group_dict[group_name] = {'group_rules':group_rules,'group_rules_egress':group_rules_egress, 'description':group.description, 'vpc_id': group.vpc_id}

    for group in security_group_dict:
        file_name = str(group)+'.yml'
        file_name = 'groups/' + env + '/' + file_name
        group_file = open(file_name, "wb")
        
        group_file.write( "---\n")
        group_file.write( "- name: %s\n" % str(group))
        group_file.write( "  hosts: localhost\n")
        group_file.write( "  tasks:\n")
        group_file.write( "  - name: %s\n" % str(group))
        group_file.write( "    local_action:\n")
        group_file.write( "      module: ec2_group\n")
        group_file.write( "      name: %s\n" % str(group))
        group_file.write( "      description: %s\n" % str(security_group_dict[group]['description']))
        group_file.write( "      vpc_id: %s\n" % str(security_group_dict[group]['vpc_id']))
        group_file.write( "      region: %s\n" % str(region))  
        group_file.write( "      profile: %s\n" % str(profile))     
        group_file.write( "      rules:\n")  
        
        if ingress == 'yes':
            for rule in security_group_dict[group]['group_rules']:
                if '-1' in str(security_group_dict[group]['group_rules'][rule]['protocol']):
                    continue
                else:
                    if '.' in str(security_group_dict[group]['group_rules'][rule]['cidr']):
                        if ',' in str(security_group_dict[group]['group_rules'][rule]['cidr']):
                            split_multiple_cidrs = str(security_group_dict[group]['group_rules'][rule]['cidr']).split(',')
                            for cidr in split_multiple_cidrs:
                                group_file.write( "        - proto: %s\n" % str(security_group_dict[group]['group_rules'][rule]['protocol'])) 
                                group_file.write( "          from_port: %s\n" % str(security_group_dict[group]['group_rules'][rule]['from_port'])) 
                                group_file.write( "          to_port: %s\n" % str(security_group_dict[group]['group_rules'][rule]['to_port'])) 
                                group_file.write( "          cidr_ip: %s\n" % cidr.replace('[', '').replace(']','')) 
                        else:
                            group_file.write( "        - proto: %s\n" % str(security_group_dict[group]['group_rules'][rule]['protocol'])) 
                            group_file.write( "          from_port: %s\n" % str(security_group_dict[group]['group_rules'][rule]['from_port'])) 
                            group_file.write( "          to_port: %s\n" % str(security_group_dict[group]['group_rules'][rule]['to_port']))                 
                            group_file.write( "          cidr_ip: %s\n" % str(security_group_dict[group]['group_rules'][rule]['cidr']).replace('[', '').replace(']','')) 
                    else:
                        group_file.write( "        - proto: %s\n" % str(security_group_dict[group]['group_rules'][rule]['protocol'])) 
                        group_file.write( "          from_port: %s\n" % str(security_group_dict[group]['group_rules'][rule]['from_port'])) 
                        group_file.write( "          to_port: %s\n" % str(security_group_dict[group]['group_rules'][rule]['to_port']))             
                        group_file.write( "          group_name: %s\n" % str(security_group_dict[group]['group_rules'][rule]['cidr']).replace('[', '').replace(']','')) 
        
        if egress == 'yes':
            group_file.write( "      rules_egress:\n") 
                     
            for rule in security_group_dict[group]['group_rules_egress']:
                if '.' in str(security_group_dict[group]['group_rules_egress'][rule]['cidr']):
                    if ',' in str(security_group_dict[group]['group_rules_egress'][rule]['cidr']):
                        split_multiple_cidrs = str(security_group_dict[group]['group_rules_egress'][rule]['cidr']).split(',')
                        for cidr in split_multiple_cidrs:
                            group_file.write( "        - proto: %s\n" % str(security_group_dict[group]['group_rules_egress'][rule]['protocol'])) 
                            group_file.write( "          from_port: %s\n" % str(security_group_dict[group]['group_rules_egress'][rule]['from_port'])) 
                            group_file.write( "          to_port: %s\n" % str(security_group_dict[group]['group_rules_egress'][rule]['to_port'])) 
                            group_file.write( "          cidr_ip: %s\n" % cidr) 
                    else:
                        group_file.write( "        - proto: %s\n" % str(security_group_dict[group]['group_rules_egress'][rule]['protocol'])) 
                        group_file.write( "          from_port: %s\n" % str(security_group_dict[group]['group_rules_egress'][rule]['from_port'])) 
                        group_file.write( "          to_port: %s\n" % str(security_group_dict[group]['group_rules_egress'][rule]['to_port']))                 
                        group_file.write( "          cidr_ip: %s\n" % str(security_group_dict[group]['group_rules_egress'][rule]['cidr']).replace('[', '').replace(']','')) 
                else:
                    group_id = str(security_group_dict[group]['group_rules_egress'][rule]['cidr']).replace('[', '').replace(']','')
                    group_file.write( "          group_id: %s\n" % group_id )

        group_file.close()
        
    print 'Groups have been generated.'    
    

if __name__ == '__main__': 
  
    parser = argparse.ArgumentParser()

    parser.add_argument('--profile', help='profile name in your ~/.boto config', required=True) 
    parser.add_argument('--env', help='environment to run script against', required=True)
    parser.add_argument('--ingress', help='options = (yes/no)', required=True)
    parser.add_argument('--egress', help='options = (yes/no)', required=True)
    parser.add_argument('--region', help='', required=True)

    args = parser.parse_args()

   
     
    main(env=args.env, profile=args.profile, ingress=args.ingress, egress=args.egress, region=args.region)

        
            

