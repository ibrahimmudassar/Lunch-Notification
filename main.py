from datetime import datetime  # For time

from discord_webhook import DiscordEmbed, DiscordWebhook  # Connect to discord
from environs import Env  # For environment variables
from selenium import webdriver  # Browser prereq
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

# Setting up environment variables
env = Env()
env.read_env()  # read .env file, if it exists


def embed_to_discord(lunch_list):
    # Webhooks to send to
    webhook = DiscordWebhook(url=env.list("WEBHOOKS"))

    # create embed object for webhook
    embed = DiscordEmbed(title="Lunch for " +
                         datetime.now().strftime("%B %d, %Y"), color="03b2f8")
    embed.set_footer(text="By Ibrahim Mudassar")
    embed.set_timestamp()

    embed.add_embed_field(name="Today's Lunch Includes:", value="".join(
        [i + "\n" for i in lunch_list]), inline=False)

    # add embed object to webhook(s)
    webhook.add_embed(embed)
    webhook.execute()


# Create new Instance of Chrome
chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = env("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")

browser = webdriver.Chrome(executable_path=env(
    'CHROMEDRIVER_PATH'), options=chrome_options)
browser.get("https://www.fdmealplanner.com/#woodbridge")

text_input = WebDriverWait(browser, 20).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "#location_9"))).click()


lunch_button = WebDriverWait(browser, 20).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "#applicationHost > div > div.menuPlanner.notranslate > div > div.page-host > div > div:nth-child(1) > div > div.mealViewerScreen > div.bg-new > div:nth-child(2) > div:nth-child(2) > div > div > div.bg-blk3 > div > div:nth-child(2)"))).click()

view_menu = WebDriverWait(browser, 20).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "#viewmpMenu"))).click()

# Tue Nov 30 2021
date_today = datetime.now().strftime("%a %b %d %Y")
lunch = WebDriverWait(browser, 20).until(
    EC.presence_of_element_located((By.NAME, date_today))).text
lunch = lunch.splitlines()[3:]  # Cleaning up unnecessary lines

browser.quit()

embed_to_discord(lunch)
