import json

import dotenv

DATABASE_PATH = "sqlite:////tmp/database.db"

settings = json.load(open("settings.json"))
secrets = dotenv.dotenv_values(".env")

DAYS_IN_A_MONTH = 30.4375
csv_filepath = "/tmp/txs.csv"

# Email vars
email_subject = "Your 2022 report is here!"
email_images_title = "Your 2022 High"
email_chart_filepath = "/tmp/chart.svg"
