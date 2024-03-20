# info about annotate.py

# This script annotates web pages for Trafilatura: (https://github.com/adbar/trafilatura).

# Dependencies: 
# - boto3
# 
# The script was written on MacOS.
# 
# The script requires you to have an AWS Athena account and Firefox installed.
# 
# It uses Common Crawl (https://commoncrawl.org). CC features an "index" offering access to random URLs. By using URLs that are evenly sampled, the test data is more balanced.
# 
# 

# Athena

# Common Crawl's archives are hosted on Amazon Web Services. They're accessible via SQL queries, through the service "Athena".

# You need to make an AWS account and enable that service. First make an admin account, then make an IAM user.
# 
# Then install the AWS command line utility. Configure it with an access token.
#
# Boto3 works as long as you have a configured AWS package.
# 

# FIREFOX

# Download Firefox if you don't have it already: (https://www.mozilla.org/en-GB/firefox/)

# Change the settings so when Firefox opens a link, it opens it in the same tab, not a new one.

# Specific steps you will need (https://support.mozilla.org/en-US/questions/1226151):

'''
    Type about:config in the Firefox address bar
    Change the browser.link.open_newwindow.restriction value to 0
    Change the browser.link.open_newwindow value to 1

'''

# Test that the configuration worked by running this command: "open -a Firefox https://www.google.com"


# (You can run this script either with "./annotate.py" or "python3 annotate.py".)



# The script retrieves 70 URLs at random from Common Crawl, opens them in Firefox, prompts the user for data, then saves it in "eval-data.py".
