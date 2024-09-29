from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import os
import time
import base64

# Create a folder for storing the PDFs
pdf_dir = "sre_book_pdfs"
if not os.path.exists(pdf_dir):
    os.makedirs(pdf_dir)

# List of chapter URLs
chapter_urls = [
    "https://sre.google/sre-book/foreword/",
    "https://sre.google/sre-book/preface/",
    "https://sre.google/sre-book/part-I-introduction/",
    "https://sre.google/sre-book/introduction/",
    "https://sre.google/sre-book/production-environment/",
    "https://sre.google/sre-book/part-II-principles/",
    "https://sre.google/sre-book/embracing-risk/",
    "https://sre.google/sre-book/service-level-objectives/",
    "https://sre.google/sre-book/eliminating-toil/",
    "https://sre.google/sre-book/monitoring-distributed-systems/",
    "https://sre.google/sre-book/automation-at-google/",
    "https://sre.google/sre-book/release-engineering/",
    "https://sre.google/sre-book/simplicity/",
    "https://sre.google/sre-book/part-III-practices/",
    "https://sre.google/sre-book/practical-alerting/",
    "https://sre.google/sre-book/being-on-call/",
    "https://sre.google/sre-book/effective-troubleshooting/",
    "https://sre.google/sre-book/emergency-response/",
    "https://sre.google/sre-book/managing-incidents/",
    "https://sre.google/sre-book/postmortem-culture/",
    "https://sre.google/sre-book/tracking-outages/",
    "https://sre.google/sre-book/testing-reliability/",
    "https://sre.google/sre-book/software-engineering-in-sre/",
    "https://sre.google/sre-book/load-balancing-frontend/",
    "https://sre.google/sre-book/load-balancing-datacenter/",
    "https://sre.google/sre-book/handling-overload/",
    "https://sre.google/sre-book/addressing-cascading-failures/",
    "https://sre.google/sre-book/managing-critical-state/",
    "https://sre.google/sre-book/distributed-periodic-scheduling/",
    "https://sre.google/sre-book/data-processing-pipelines/",
    "https://sre.google/sre-book/data-integrity/",
    "https://sre.google/sre-book/reliable-product-launches/",
    "https://sre.google/sre-book/part-IV-management/",
    "https://sre.google/sre-book/accelerating-sre-on-call/",
    "https://sre.google/sre-book/dealing-with-interrupts/",
    "https://sre.google/sre-book/operational-overload/",
    "https://sre.google/sre-book/communication-and-collaboration/",
    "https://sre.google/sre-book/evolving-sre-engagement-model/",
    "https://sre.google/sre-book/part-V-conclusions/",
    "https://sre.google/sre-book/lessons-learned/",
    "https://sre.google/sre-book/conclusion/",
    "https://sre.google/sre-book/availability-table/",
    "https://sre.google/sre-book/service-best-practices/",
    "https://sre.google/sre-book/incident-document/",
    "https://sre.google/sre-book/example-postmortem/",
    "https://sre.google/sre-book/launch-checklist/",
    "https://sre.google/sre-book/production-meeting/",
    "https://sre.google/sre-book/bibliography/"
]


# Function to configure Chrome options for headless browsing
def get_chrome_options():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    return chrome_options


# Function to download a webpage as PDF using DevTools Protocol
def download_page_as_pdf(url, pdf_filename):
    # Initialize Chrome with options
    chrome_options = get_chrome_options()
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        # Open the web page
        driver.get(url)
        time.sleep(3)  # Allow some time for the page to load

        # Get the DevTools session for issuing commands
        chrome_session = driver.execute_cdp_cmd("Page.enable", {})

        # Save the page as PDF using the DevTools Protocol
        result = driver.execute_cdp_cmd("Page.printToPDF", {
            "printBackground": True,
            "format": "A4"
        })

        # Decode the base64-encoded PDF content and save it to a file
        with open(pdf_filename, "wb") as file:
            file.write(base64.b64decode(result['data']))

        print(f"Saved {pdf_filename} from {url}")
    except Exception as e:
        print(f"Error saving {pdf_filename}: {e}")
    finally:
        # Close the browser
        driver.quit()


# Iterate over chapter URLs and save each as a PDF
for url in chapter_urls:
    chapter_name = url.split('/')[-2].replace('-', '_')  # Extract chapter name from URL
    pdf_filename = os.path.join(pdf_dir, f"{chapter_name}.pdf")
    download_page_as_pdf(url, pdf_filename)
