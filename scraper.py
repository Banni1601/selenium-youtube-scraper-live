import smtplib
#import pandas as pd
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

YOUTUBE_TRENDING_URL = 'https://www.youtube.com/feed/trending'


def get_driver():
  chrome_options = Options()
  chrome_options.add_argument('--no-sandbox')
  chrome_options.add_argument('--headless')
  chrome_options.add_argument('--disable-dev-shm-usage')
  driver = webdriver.Chrome(options=chrome_options)
  return driver


def get_videos(driver):
  VIDEO_DIV_TAG = 'ytd-video-renderer'
  driver.get(YOUTUBE_TRENDING_URL)
  videos = driver.find_elements(By.TAG_NAME, VIDEO_DIV_TAG)
  return videos


def parse_video(video):
  title_tag = video.find_element(By.ID, 'video-title')
  title = title_tag.text
  url = title_tag.get_attribute('href')

  thumbnail_tag = video.find_element(By.TAG_NAME, 'img')
  thumbnail_url = thumbnail_tag.get_attribute('src')

  Channel_div = video.find_element(By.CLASS_NAME, 'ytd-channel-name')
  channel_name = Channel_div.text

  description = video.find_element(By.ID, 'description-text').text
  return {
      'title': title,
      'url': url,
      'thumbnail_url': thumbnail_url,
      'channel': channel_name,
      'description': description
  }


def send_email(body):
  MY_EMAIL = 'banniv2024@gmail.com'
  MY_PASSWORD = 'uvkg yphh fjfn tflz'

  # Create the email
  msg = MIMEMultipart()
  msg['From'] = MY_EMAIL
  msg['To'] = MY_EMAIL
  msg['Subject'] = 'MAIL SENT FROM THE REPLIT'

  # Attach the email body
  body = body
  msg.attach(MIMEText(body, 'plain'))

  try:
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as connection:
      connection.login(user=MY_EMAIL, password=MY_PASSWORD)
      connection.sendmail(from_addr=MY_EMAIL,
                          to_addrs=MY_EMAIL,
                          msg=msg.as_string())
    print("Mail was successfully sent")
  except Exception as e:
    print(f'Error: {e}')


if __name__ == "__main__":
  print('Creating a driver')
  driver = get_driver()

  print('Fetching trending videos')
  videos = get_videos(driver)

  print(f'Found {len(videos)} videos')

  print('Parsing the top 10 video')
  videos_data = [parse_video(video) for video in videos[:10]]

  #print('Save the data to a CSV')
  #videos_df = pd.DataFrame(videos_data)
  #print(videos_df)
  #videos_df.to_csv('trending.csv', index=None)
  print('Sending the email')
  body = json.dumps(videos_data, indent=2)
  send_email(body)
