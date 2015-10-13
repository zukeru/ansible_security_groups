# Ansible Security Group State-file Janitor Plugin
### by Grant Zukel

#Introduction:
The security group plugin is designed to aquire AWS security groups by environment and save them into ansible playbook files as state files. This is designed to help you maintain your AWS security groups.

----------

When executed with the right parameters the security_groups.py will retrieve all security_groups from aws with their relations and save them into their own directory by environment.


----------


The default directory will be in: 
 * groups/env/securitygroup.yml


----------


When the yml file is run it will reset whatever is in EC2 to whatever is in the playbookfile. If the security group doesn’t exist it will create the group with the rules defined.


----------


The groups stored in this repo are the state file for the current environment. Thus, if the state files exist for the environment in question do not run the security_group.py as it will overwrite whatever is there.


----------


#Installation:


----------


To install clone the repo into the directory of your choosing. Replace your boto file with the file included in the repo. Simply insert your credentials for the environments respectively.

----------



#How to Use:

### If the state files do not exist, or you want to create a new environment please run the python file security_groups.py with the appropriate arguments! Please see below for an explanation of arguments.

----------


Then you will want to run the python script security_groups.py with the following arguments:

----------


    python security_groups.py --profile scratch --region us-west-2 --ingress yes --egress no --env scratch

----------


 * profile = boto profile to use, also the profile that will be inserted into the security group yml files. This is also why we have included the template file to standardize. boto across all users. Otherwise each user will have to change the yml file and that is not the intention of this script.

----------


 * region = aws region

----------


* env = this wil be the name of the folder the program saves the security groups for. If you want to run it for an existing environment simply change the env name.
 * ingress = whether or not to include the ingress rules: options yes or no please use lower case.

----------


 * egress - whether or not to include the egress rules: options yes or no please use lower case.

----------


###If you have changed the state file and wish to reset an environment to the state files run execute_group_pb.sh with the appropriate arguments.

----------


Then to execute a play book run the following bash script.

----------


###Run a single playbook to reset a single group:
    ./execute_group_pb.sh test.yml scratch
this will look for a file in groups/scratch/test.yml

----------


The first argument is the name of the playbook you wish to run, use all to run recursively over an entire directory.

----------


The second argument is the environment name you wish to use. This will look at groups/environment you pass for the groups.

----------


###Reset an entire environment:
    ./execute_group_pb.sh all environment

----------


The first argument is the playbook here, the all flag is what tells it to run against all playbooks in the environment. 

----------


The second argument is the environment to run. This will look at the directory groups/environment for the playbooks and recursively loop and execute them.

----------

#Workflow:

##The workflow for the security groups is as follows.


###Master Branch: The master branch is the state of the environment. 

###To make a change:
----------

In order to make a change, please create a branch. Then simply make your change, commit to your branch and create a pull request. 

----------

Once the pull request is merged switch back to master on your local machine update your local files to the master and run the playbooks accordingly. 



#Cleanup Unused Security Groups:

##This script will either display or delete unused and used security group based on python arguments.

###What is it?
----------
This script will connect AWS and look for security groups that are currently not in use. If the security group is not currently in use the program will then delete the security group if the --delete yes is passed to the script.


###How to run:
----------

python cleanup.py --region us-west-2 --delete no --profile scratch

----------

###Sample output of what to expect with no delete flag set:

----------
	The list of security groups to be removed is below.
	Run this again with `--delete` to remove them
	[   u'1pauth',
	    u'1pprofile',
	    u'ES-elasticsearch-scratch-Scratch-Client-N0wZeA_V',
	    u'JWFRemote',
	    u'KAFKA-1p-kafka-zookeeper-snapshot-Scratch-Kafka-KYhp77eb',
	    u'KAFKA-1p-kafka-zookeeper-snapshot-Scratch-Kafka-eRzgAn84',
	    u'KAFKA-1p-kafka-zookeeper-snapshot-Scratch-Kafka-fwNhN2g1',
	    u'dat_1pauth',
	    u'developer_access',
	    u'eelb',
	    u'elb',
	    u'example',
	    u'graylog-graylog-elasticsearch-scratch-Scratch-client-u5msr5Ww',
	    u'infra_asgard',
	    u'infra_bastion',
	    u'launch-wizard-1',
	    u'launch-wizard-2',
	    u'launch-wizard-3',
	    u'mid_1pauth',
	    u'mid_1pprofile',
	    u'mid_1pzuul',
	    u'mongo-db',
	    u'simian-army',
	    u'test',
	    u'test2',
	    u'test3',
	    u'test4',
	    u'wos_access']
	Total of 28 groups targeted for removal.
	[u'cost_savings_test', u'infra_eureka', u'default', u'graylog', u'bastion_access']
