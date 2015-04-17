##  A Jenkins project to build and deploy mcare-web on Pivotal Cloud Foundry


#### Create a Project Backup

Jenkins Project backup was creatd from Jenkins using a browser

https://pivotal-cloudbees.23.92.225.219.xip.io/job/mCare/config.xml

Save the config.xml file.


#### Restore backup to Jenkins

Use a REST client such as the Firefox RestClient plugin

Note: If this is an initial deploy to Jenkins, not a restore of an existing project,
then a project must be created in Jenkins first using the jenkins UI

After plugin is installed and a Jenkins project exists

In Firefox
Tools-> RestClient

For example if job name is mCare

Post to  http://23.92.225.171:8100/job/mCare/config.xml

Body Field:  Paste the xml containing the jenkins project into the Body field 


#### Configure GitHub to Call Jenkins


In the github project click project settings on the right
select the  'WebHooks and Services' entry in the left menu
click the 'Add Service' button
Select  'Jenkins (Github plugin)' from the dropdown list

Set the 'jenkins hook url' field to 
https://pivotal-cloudbees.23.92.225.219.xip.io/github-webhook/

check the Active checkbox.


When this configuration is complete, GitHub will notify Jenkins 
whenever a commit is made to the repository .
