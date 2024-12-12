# cloud-status

This script monitors RSS feeds for status updates from AWS and Azure and sends notifications via AWS SNS when updates are detected. It works by comparing the current RSS feed data with previously saved data.


## Prerequisites

1. **Python Environment**: Ensure Python 3 is installed
2. Provide AWS role to SNS for the running instance
3. **SNS Topic**:
   - Create an SNS topic in same AWS account.
   - Update the script with your SNS topic's ARN.
  

## Installation
1. Can use basic ec2 insace like t2 micro
1. Clone this repository.
2. Install the required Python library:
   ```
   pip install requests boto3
   ```
## Configuration

`SNS_TOPIC_ARN`: update the ARN for sns topic in the script.

## How It Works

1. **Fetch Feed**: The script fetches the RSS feed from the URLs specified for the cloud.
2. **Check for Updates**:
   - It compares the line count of the current feed with the previously stored count.
   - If the line count has changed, it saves the updated feed locally and sends a notification.
3. **Send Notification**:
   - Sends a custom email notification via the configured SNS topic.

## Limitations

- The script compares feeds based on line count. Minor changes (like character change) may not trigger an update, but minor changes will not occur for staus update.
- Once notification received check cloud status page for detecting change, if needed to verify the change can refer the updated file txt present in the running instance
