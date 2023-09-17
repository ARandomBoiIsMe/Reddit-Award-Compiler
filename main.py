from utils import config_util, reddit_util
from dataclasses import dataclass
import re
import time
import xlsxwriter

config = config_util.load_config()
reddit = reddit_util.initialize_reddit(config)

@dataclass
class Award():
    award_date: str
    award_name: str
    permalink: str
    award_gifter: str

def main():
    award_message_subject_regex = r"Your (comment|post) has been given the (.+?) Award!"
    award_message_body_regex = r"(An anonymous redditor|u/(\w+)) liked \[your (comment|post)\]\((.+?)\) so much that they\'ve given it the (.+?) Award\."

    awards = []
    for item in reddit.inbox.messages(limit=None):
        # Skip message if it's not an Award Message
        message_subject_match = re.search(award_message_subject_regex, item.subject)
        if message_subject_match is None:
            continue

        # Skip message if relevant info can't be retrieved from message body
        message_body_match = re.search(award_message_body_regex, item.body)
        if message_body_match is None:
            continue

        # Getting relevant info from message body
        award_name = message_subject_match.group(2)
        permalink = message_body_match.group(3)
        award_time_received = time.localtime(item.created_utc)
        award_gifter = None
        if message_body_match.group(1) == "An anonymous redditor":
            award_gifter = "Unknown"
        else:
            award_gifter = message_body_match.group(1)

        awards.append(Award(award_date=f"{award_time_received.tm_mday}-{award_time_received.tm_mon}-{award_time_received.tm_year}",
                            award_name=award_name,
                            permalink=permalink,
                            award_gifter=award_gifter
                        )
                    )
        

    save_to_excel(awards)

def save_to_excel(awards):
    # New Workbook Instance
    workbook = xlsxwriter.Workbook("RedditAwards.xlsx")
    worksheet = workbook.add_worksheet("Sheet #1")

    # Add a bold format to use to highlight cells.
    bold = workbook.add_format({'bold': True})

    # Set titles in file
    worksheet.write(0, 0, "Award Grant Date", bold)
    worksheet.write(0, 1, "Award Name", bold)
    worksheet.write(0, 2, "Award Gifter", bold)
    worksheet.write(0, 3, "Post/Comment Link", bold)

    # Write data to file
    for i in range(len(awards)):
        worksheet.write(i + 1, 0, awards[i].award_date)
        worksheet.write(i + 1, 1, awards[i].award_name)
        worksheet.write(i + 1, 2, awards[i].award_gifter)
        worksheet.write(i + 1, 3, awards[i].permalink)

    workbook.close()

if __name__ == "__main__":
    main()