import sys
import time
import schedule

sys.path.append("D:/python/jervis")

from Linkedin_file.Linkedin_Article_store import analyze_and_store_for_linkedin
from Website_automation.blog_store import analyze_and_store_content_for_website
from Website_automation.post_blog_in_website import post_category_blog
from backend.chatbot import ChatBot

def auto_1():
    try:
        print("[AUTO] Generating blog article using ChatBot...")
        ChatBot("i need an article about data analyst and more than 350 words")

        time.sleep(10)

        print("[AUTO] Analyzing and storing blog content...")
        analyze_and_store_content_for_website()

        time.sleep(10)

        print("[AUTO] Posting blog to website...")
        post_category_blog("data_analysis", post_index=0, status='publish')

        print("[AUTO] Blog post automation completed.")
    except Exception as e:
        print(f"[AUTO ERROR] {e}")


# 🕓 Schedule: every day at 10:00 AM
schedule.every().day.at("23:27").do(auto_1)

def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(60)


# if __name__ == "__main__":
#     print("[AUTO SYSTEM] Scheduler is running...")
#     while True:
#         schedule.run_pending()
#         time.sleep(60)


