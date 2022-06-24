import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from jinja2 import Environment, FileSystemLoader, select_autoescape
from pandas import DataFrame

from stori.content import calculate_stats, make_content
from stori.config import secrets, settings
from stori.helpers import thousand_separator


def make_template(data: dict) -> str:
    """Makes html template"""
    env = Environment(
        loader=FileSystemLoader("stori/templates"),
        autoescape=select_autoescape(["html", "xml"]),
    )
    env.filters["thousand_separator"] = thousand_separator
    template = env.get_template("email.html")
    html = template.render(data)
    return html


def write_file(html):
    html_file = open("test.html", "w")
    _ = html_file.write(html)
    html_file.close()


def process_data(user_name: str, df: DataFrame) -> dict:
    stats = calculate_stats(df)
    body = make_content(stats)
    html = make_template(
        {"name": user_name, "body": body, "settings": {"months_to_show": settings["months_to_show_in_email"]}}
    )
    data = {"html": html, "text": ""}
    return data


def send_email(email_receiver: str, subject: str, content: dict) -> str:
    if settings["dry_run"]:
        write_file(content["html"])
        return "Dry Run enabled. File saved."
    else:
        em = MIMEMultipart("alternative")
        em.attach(MIMEText(content["text"], "plain"))
        em.attach(MIMEText(content["html"], "html"))
        em["From"] = secrets["MAIL_USERNAME"]
        em["To"] = email_receiver
        em["Subject"] = subject
        context = ssl.create_default_context()
        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls(context=context)
            server.login(secrets["MAIL_USERNAME"], secrets["MAIL_PASSWORD"])
            server.sendmail(secrets["MAIL_USERNAME"], email_receiver, em.as_string())
        except Exception as e:
            print(e)
        return em.as_string()
