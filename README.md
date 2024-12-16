# cloud-status

This script monitors RSS feeds for status updates from AWS and Azure and sends notifications via AWS SNS when updates are detected. It works by comparing the current RSS feed data with previously saved data.


## Prerequisites

1. **Python Environment**: Ensure Python 3 is installed
2. Provide AWS role to SNS for the running instance
3. **SNS Topic**:
   - Create an SNS topic in same AWS account.
   - Update the script with your SNS topic's ARN.
  

## Installation
1. Can use amazon linux basic ec2 instance like type t2 micro / or can use lambda

2. Clone this repository.
3. Install the required Python library:
   ```
   pip install requests boto3
   ```
4. Setup cron for execution
   sample one $ crontab -l
               0 * * * * /usr/bin/python3 /home/ec2-user/scripts/cloud-status/status_update.py >> /home/ec2-user/scripts/cloud-status/status_update.log 2>&1
   and logs will be availablke at  /home/ec2-user/scripts/cloud-status/status_update.log
    
## Configuration

`SNS_TOPIC_ARN`: update the ARN for sns topic in the script.

## How It Works

1. **Fetch Feed**: The script fetches the RSS feed from the URLs specified for the cloud.
2. **Check for Updates**:
   - It compares the line count of the current feed with the previously stored count.
   - If the line count has changed, it saves the updated feed locally and sends a notification.
3. **Send Notification**:
   - Sends a custom email notification via the configured SNS topic.
     

## Alternative method for ec2

The same code with minor modification can use in lambda for the same use case, and can trigger SNS for sending notifications.

## Troublehsooting and logging 

Fetched data is stored in the /tmp directory on the same instance. If manual comparison is needed for troubleshooting, both the current and updated feed files will be available for reference on the instance.
