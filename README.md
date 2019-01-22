# cloud9

TIPS:
    We recommend the following best practices for using your AWS Cloud9 environment
    •	Use source control and backup your environment frequently. AWS Cloud9 does not perform automatic backups.
    •	Perform regular updates of software on your environment. AWS Cloud9 does not perform automatic updates on your behalf.
    •	Turn on AWS CloudTrail in your AWS account to track activity in your environment.
    •	Only share your environment with trusted users. Sharing your environment may put your AWS access credentials at risk.

Quick Start

    Note: Please create your project folder under cloud9 parent repostory. It is setup to link with https://github.com/ltiew/cloud9.git.

    1) In Clound IDE, select Window->New Terminal
    2) cd cloud9
    3) git checkout -b dev # this with switch to dev branch


Note:
    F3 Python SDK 8.0 is installed under ~environment/cloud9 virtual environment.
    Sample toy valuation example can be fond in ~environment/cloud9/Python/valuation.py
    
WARNING !!!

    Please do not push any private or sensitive information into this public repository.