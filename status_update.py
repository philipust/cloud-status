import requests
import boto3

FEED_URL_AWS = "https://status.aws.amazon.com/rss/all.rss"
FEED_URL_AZURE = "https://azure.status.microsoft/en-in/status/feed/"
LINE_COUNT_FILE_AWS = "/tmp/rss_last_count_aws.txt"
LINE_COUNT_FILE_AZURE = "/tmp/rss_last_count_azure.txt"
CURRENT_FEED_FILE_AWS = "/tmp/current_aws.txt"
UPDATED_FEED_FILE_AWS = "/tmp/updated_aws.txt"
CURRENT_FEED_FILE_AZURE = "/tmp/current_azure.txt"
UPDATED_FEED_FILE_AZURE = "/tmp/updated_azure.txt"
SNS_TOPIC_ARN = "arn:aws:sns:us-east-1:149536489917:rss-update"

status_page_aws = "https://health.aws.amazon.com/health/status"
status_page_azure = "https://azure.status.microsoft/en-in/status"

#function for fetching data from the clpud feed url

def fetch(feed_url):
    try:
        response = requests.get(feed_url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching feed: {e}")
        return None

def line(feed):
    return len(feed.splitlines())

def save_feed(feed, file_path):
    with open(file_path, "w") as file:
        file.write(feed)


#function to send notification via SNS realated with update

def send_sns_notification(topic_arn, subject, message):
    try:
        sns_client = boto3.client("sns", region_name="us-east-1")
        sns_client.publish(TopicArn=topic_arn, Subject=subject, Message=message)
        print("Notification sent via SNS.")
    except Exception as e:
        print(f"Error sending SNS notification: {e}")


#function to check update in feed and added notification message

def check(last_count, current_feed, current_feed_file, updated_feed_file, feed_name, status_page_url, feed_url):
    if not current_feed:
        print("No feed fetched. Exiting.")
        return last_count

    current_count = line(current_feed)
    print(f"Current Line Count: {current_count}")
    save_feed(current_feed, current_feed_file)

    if current_count != last_count:
        print("Feed has been updated!")
        save_feed(current_feed, updated_feed_file)
        subject = f"Attention! {feed_name} Status Page Updated"
        message = f"""
Hello Team,

The {feed_name} status page has been updated. Please check the following link for more details.
{status_page_url}

An update has been detected from the status feed URL for the cloud:  {feed_url}

        
Thank you.
"""
        send_sns_notification(
            SNS_TOPIC_ARN, subject , message
        )
        return current_count
    else:
        print("No updates detected.")
        return last_count

def save(count, file_path):
    with open(file_path, "w") as file:
        file.write(str(count))

def load(file_path):
    try:
        with open(file_path, "r") as file:
            return int(file.read().strip())
    except FileNotFoundError:
        return 0

#main blcok for executing feed check for both azure and aws
if __name__ == "__main__":
    last_count_aws = load(LINE_COUNT_FILE_AWS)
    current_feed_aws = fetch(FEED_URL_AWS)
    last_count_aws = check(last_count_aws, current_feed_aws, CURRENT_FEED_FILE_AWS, UPDATED_FEED_FILE_AWS, "AWS", status_page_aws, FEED_URL_AWS)
    save(last_count_aws, LINE_COUNT_FILE_AWS)

    last_count_azure = load(LINE_COUNT_FILE_AZURE)
    current_feed_azure = fetch(FEED_URL_AZURE)
    last_count_azure = check(last_count_azure, current_feed_azure, CURRENT_FEED_FILE_AZURE, UPDATED_FEED_FILE_AZURE, "Azure", status_page_azure, FEED_URL_AZURE)
    save(last_count_azure, LINE_COUNT_FILE_AZURE)

