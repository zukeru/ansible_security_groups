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


