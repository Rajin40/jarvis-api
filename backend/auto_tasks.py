import sys
import time
import schedule

sys.path.append("D:/python/jervis")

from Linkedin_file.Linkedin_Article_store import analyze_and_store_for_linkedin
from Website_automation.blog_store import analyze_and_store_content_for_website
from Website_automation.post_blog_in_website import post_category_blog
from backend.chatbot import ChatBot

def auto_data_analyst():
    try:
        print("[AUTO] Generating blog article using ChatBot...")
        ChatBot("Write a comprehensive blog post of at least 1500 words on the topic Data Analyst. The blog should be well-structured, SEO-optimized, and engaging for readers interested in data careers, technology, and analytics.")

        time.sleep(10)

        print("[AUTO] Analyzing and storing blog content...")
        analyze_and_store_content_for_website()

        time.sleep(10)

        print("[AUTO] Posting blog to website...")
        post_category_blog("data_analysis", post_index=0, status='publish')

        print("[AUTO] Blog post automation completed.")
    except Exception as e:
        print(f"[AUTO ERROR] {e}")


def auto_data_science():
    try:
        print("[AUTO] Generating blog article using ChatBot...")
        ChatBot("Generate a comprehensive, SEO-focused blog post (1500+ words) on “Data Science in the Modern Era”. Structure the content with a powerful introduction, followed by in-depth sections on: the definition of data science, its business relevance, key tools (Python, SQL, Jupyter, etc.), data pipelines, AI integration, real-world use cases, and emerging trends. Include insights into required skills, certifications, and career paths. Optimize for keywords like “data science applications”, “tools used in data science”, and “data science career roadmap”.")

        time.sleep(10)

        print("[AUTO] Analyzing and storing blog content...")
        analyze_and_store_content_for_website()

        time.sleep(10)

        print("[AUTO] Posting blog to website...")
        post_category_blog("data_analysis", post_index=0, status='publish')

        print("[AUTO] Blog post automation completed.")
    except Exception as e:
        print(f"[AUTO ERROR] {e}")


def auto_Web_Development():
    try:
        print("[AUTO] Generating blog article using ChatBot...")
        ChatBot("Write a long-form (1500+ words), SEO-optimized blog post on “The Future of Web Development: Frameworks, Trends & Best Practices”. Cover front-end vs back-end development, modern stacks (MERN, JAMstack), responsive design, performance optimization, accessibility, and CI/CD workflows. Highlight tools like React, Tailwind CSS, GitHub Actions, and Vite. Discuss freelancing vs agency paths and tips for staying relevant in a rapidly evolving field. Use keywords such as “modern web development”, “best web frameworks 2025”, and “web development roadmap”.")

        time.sleep(10)

        print("[AUTO] Analyzing and storing blog content...")
        analyze_and_store_content_for_website()

        time.sleep(10)

        print("[AUTO] Posting blog to website...")
        post_category_blog("data_analysis", post_index=0, status='publish')

        print("[AUTO] Blog post automation completed.")
    except Exception as e:
        print(f"[AUTO ERROR] {e}")


def auto_web_development():
    try:
        print("[AUTO] Generating blog article using ChatBot...")
        ChatBot("Write a long-form (1500+ words), SEO-optimized blog post on “The Future of Web Development: Frameworks, Trends & Best Practices”. Cover front-end vs back-end development, modern stacks (MERN, JAMstack), responsive design, performance optimization, accessibility, and CI/CD workflows. Highlight tools like React, Tailwind CSS, GitHub Actions, and Vite. Discuss freelancing vs agency paths and tips for staying relevant in a rapidly evolving field. Use keywords such as “modern web development”, “best web frameworks 2025”, and “web development roadmap”.")

        time.sleep(10)

        print("[AUTO] Analyzing and storing blog content...")
        analyze_and_store_content_for_website()

        time.sleep(10)

        print("[AUTO] Posting blog to website...")
        post_category_blog("data_analysis", post_index=0, status='publish')

        print("[AUTO] Blog post automation completed.")
    except Exception as e:
        print(f"[AUTO ERROR] {e}")


def auto_graphic_design():
    try:
        print("[AUTO] Generating blog article using ChatBot...")
        ChatBot("Create a detailed and keyword-rich blog post (1500+ words) on “Mastering Graphic Design in the Digital Age”. Include sections on visual hierarchy, typography, color psychology, branding strategy, UX design overlap, and portfolio development. Feature top tools (Figma, Adobe Illustrator, Canva, Photoshop), common use cases (social media, branding, UI), and tips for building a freelance or agency design career. Target keywords like “modern graphic design trends”, “tools for graphic designers”, and “how to become a graphic designer”.")

        time.sleep(10)

        print("[AUTO] Analyzing and storing blog content...")
        analyze_and_store_content_for_website()

        time.sleep(10)

        print("[AUTO] Posting blog to website...")
        post_category_blog("data_analysis", post_index=0, status='publish')

        print("[AUTO] Blog post automation completed.")
    except Exception as e:
        print(f"[AUTO ERROR] {e}")


def auto_Graphic_Design():
    try:
        print("[AUTO] Generating blog article using ChatBot...")
        ChatBot("Create a detailed and keyword-rich blog post (1500+ words) on “Mastering Graphic Design in the Digital Age”. Include sections on visual hierarchy, typography, color psychology, branding strategy, UX design overlap, and portfolio development. Feature top tools (Figma, Adobe Illustrator, Canva, Photoshop), common use cases (social media, branding, UI), and tips for building a freelance or agency design career. Target keywords like “modern graphic design trends”, “tools for graphic designers”, and “how to become a graphic designer”.")

        time.sleep(10)

        print("[AUTO] Analyzing and storing blog content...")
        analyze_and_store_content_for_website()

        time.sleep(10)

        print("[AUTO] Posting blog to website...")
        post_category_blog("data_analysis", post_index=0, status='publish')

        print("[AUTO] Blog post automation completed.")
    except Exception as e:
        print(f"[AUTO ERROR] {e}")


def auto_market_analysis():
    try:
        print("[AUTO] Generating blog article using ChatBot...")
        ChatBot("Write a data-driven, SEO-optimized blog article (1500+ words) titled “Market Analysis: How Businesses Make Smarter Strategic Decisions”. Explain the fundamentals, types (qualitative vs quantitative, competitive analysis, SWOT), and tools (Google Trends, Excel, Tableau, SEMrush). Provide frameworks for segmenting markets and evaluating opportunities. Include real business examples and strategic takeaways. Focus on keywords like “how to conduct a market analysis”, “market analysis tools”, and “market trends analysis for business”.")

        time.sleep(10)

        print("[AUTO] Analyzing and storing blog content...")
        analyze_and_store_content_for_website()

        time.sleep(10)

        print("[AUTO] Posting blog to website...")
        post_category_blog("data_analysis", post_index=0, status='publish')

        print("[AUTO] Blog post automation completed.")
    except Exception as e:
        print(f"[AUTO ERROR] {e}")



def auto_market_research():
    try:
        print("[AUTO] Generating blog article using ChatBot...")
        ChatBot("Produce a 1500+ word authoritative blog post on “Market Research Strategies: From Data Collection to Business Impact”. Cover primary vs secondary research, research design, survey creation, competitor benchmarking, audience profiling, and interpreting insights. Mention tools like Statista, SurveyMonkey, Think with Google, and brand trackers. Emphasize practical use cases in product development and marketing strategy. Optimize for terms like “market research methods”, “importance of market research”, and “tools for market research analysis”.")

        time.sleep(10)

        print("[AUTO] Analyzing and storing blog content...")
        analyze_and_store_content_for_website()

        time.sleep(10)

        print("[AUTO] Posting blog to website...")
        post_category_blog("data_analysis", post_index=0, status='publish')

        print("[AUTO] Blog post automation completed.")
    except Exception as e:
        print(f"[AUTO ERROR] {e}")



def auto_digital_marketing():
    try:
        print("[AUTO] Generating blog article using ChatBot...")
        ChatBot("Generate a deep-dive blog article (1500+ words) on “Digital Marketing in 2025: Multi-Channel Strategy, Automation & AI”. Include core components (SEO, content marketing, PPC, email, social media), major tools (Google Analytics 4, SEMrush, HubSpot, Meta Ads), funnel strategy, KPIs, and AI-powered personalization. Compare B2B vs B2C strategies, and end with future trends like voice search, zero-click content, and marketing automation. Optimize for terms like “digital marketing trends 2025”, “best digital marketing tools”, and “how to build a digital marketing strategy”.")

        time.sleep(10)

        print("[AUTO] Analyzing and storing blog content...")
        analyze_and_store_content_for_website()

        time.sleep(10)

        print("[AUTO] Posting blog to website...")
        post_category_blog("data_analysis", post_index=0, status='publish')

        print("[AUTO] Blog post automation completed.")
    except Exception as e:
        print(f"[AUTO ERROR] {e}")

def auto_statistical_analysis():
    try:
        print("[AUTO] Generating blog article using ChatBot...")
        ChatBot("Write a detailed, keyword-optimized blog post (1500+ words) on “Mastering Statistical Analysis for Business and Research in 2025”. Cover key concepts (descriptive vs inferential statistics), essential techniques (hypothesis testing, regression, ANOVA, chi-square), and practical applications in industries like marketing, healthcare, and finance. Discuss popular tools such as SPSS, R, Python, and Excel. Include sections on data preparation, assumptions checking, and result interpretation. Provide guidance on learning paths, certifications, and portfolio tips. Use SEO keywords like “statistical analysis methods”, “tools for statistical analysis”, and “how to learn statistical analysis”.")

        time.sleep(10)

        print("[AUTO] Analyzing and storing blog content...")
        analyze_and_store_content_for_website()

        time.sleep(10)

        print("[AUTO] Posting blog to website...")
        post_category_blog("data_analysis", post_index=0, status='publish')

        print("[AUTO] Blog post automation completed.")
    except Exception as e:
        print(f"[AUTO ERROR] {e}")

def run_all_jobs_every_30_seconds():
    job_functions = [
        auto_data_analyst,
        auto_data_science,
        auto_web_development,
        auto_graphic_design,
        auto_market_analysis,
        auto_market_research,
        auto_digital_marketing,
        auto_statistical_analysis
    ]

    while True:
        for job in job_functions:
            job()
            print("[WAIT] Waiting 30 seconds before next job...\n")
            time.sleep(30)

schedule.every().day.at("22:00").do(run_all_jobs_every_30_seconds)

if __name__ == "__main__":
    print("[AUTO SYSTEM] Running all blog tasks every 30 seconds...")
    run_all_jobs_every_30_seconds()