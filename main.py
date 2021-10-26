from datetime import datetime  # For time

from discord_webhook import DiscordEmbed, DiscordWebhook  # Connect to discord
from environs import Env  # For environment variables
from selenium import webdriver  # Browser prereq
from selenium.common.exceptions import NoSuchElementException  # Exception for selenium
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


# Setting up environment variables
env = Env()
env.read_env()  # read .env file, if it exists


# I use opengraph to simplify the collection process
def embed_to_discord(main, main_desc, alt, alt_desc):
    # Webhooks to send to
    webhook = DiscordWebhook(url=env.list("WEBHOOKS"))

    # create embed object for webhook
    embed = DiscordEmbed(title="Lunch for " + datetime.now().strftime("%B %d, %Y"),
                         description="Today's Lunch Includes:", color="03b2f8")
    embed.set_footer(text="By Ibrahim Mudassar")
    embed.set_timestamp()

    embed.add_embed_field(name="Main Entree - " + main,
                          value=main_desc, inline=False)
    embed.add_embed_field(name="Alternate - " + alt,
                          value=alt_desc, inline=False)

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
browser.get("https://woodbridge.nutrislice.com/menu/john-f-kennedy-memorial-high-school/lunch/" +
            datetime.now().strftime("%Y-%m-%d"))

try:
    WebDriverWait(browser, 20).until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, "#content > div > div.splash-container > button"))).click()

except NoSuchElementException:
    pass


entree = WebDriverWait(browser, 20).until(EC.presence_of_element_located(
    (By.CSS_SELECTOR, "#content > ns-menu > div > div.type-container > div > ns-menu-day-loader > div > div > ns-menu-day > div > ns-menu-section > ns-menu-day-section > ul > li:nth-child(1) > ns-menu-station > ul > li > ns-menu-item > div > div > ns-menu-item-food > div > div > a > div > div > span"))).text

entree_description = WebDriverWait(browser, 20).until(EC.presence_of_element_located(
    (By.CSS_SELECTOR, "#content > ns-menu > div > div.type-container > div > ns-menu-day-loader > div > div > ns-menu-day > div > ns-menu-section > ns-menu-day-section > ul > li:nth-child(1) > ns-menu-station > ul > li > ns-menu-item > div > div > ns-menu-item-food > div > div > a > div > p"))).text

alternate = WebDriverWait(browser, 20).until(EC.presence_of_element_located(
    (By.CSS_SELECTOR, "#content > ns-menu > div > div.type-container > div > ns-menu-day-loader > div > div > ns-menu-day > div > ns-menu-section > ns-menu-day-section > ul > li:nth-child(2) > ns-menu-station > ul > li > ns-menu-item > div > div > ns-menu-item-food > div > div > a > div > div > span"))).text

alternate_description = WebDriverWait(browser, 20).until(EC.presence_of_element_located(
    (By.CSS_SELECTOR, "#content > ns-menu > div > div.type-container > div > ns-menu-day-loader > div > div > ns-menu-day > div > ns-menu-section > ns-menu-day-section > ul > li:nth-child(2) > ns-menu-station > ul > li > ns-menu-item > div > div > ns-menu-item-food > div > div > a > div > p"))).text

embed_to_discord(entree, entree_description, alternate, alternate_description)

browser.quit()
