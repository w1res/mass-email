"""
Developed by w1res && vx1

Generate bulk temporary email
Usage: python3 main.py --amounts 50 --password ContaPobre1337++

Alternative usage using Proxychains4: proxychains4 -q python3 main.py -a 50 -p ContaPobre1337++
OBS: Slow, but it prevents you from getting the API lock.
"""

import asyncio
import platform
import random
import re
from argparse import ArgumentParser
from json import dumps
from typing import Mapping

import aiohttp
from faker import Faker
from rich.console import Console
from rich.prompt import Prompt

from src.interface import ui

console = Console()


async def request_post(url: str, d: dict, h: dict) -> dict:
    """Make a request with the POST method returning a dictionary."""

    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=dumps(d), headers=h) as response:
            return await response.json()


def username_generator() -> str:
    """Return a random username."""

    fake = Faker()  # Initialize a generator

    random_name = fake.name()
    name = re.sub(r"\s+", "", random_name)  # Remove whitespace

    random_number: int = random.randint(1, 99999)
    extension_email: str = "@candassociates.com"
    username: str = f"{name}{random_number}{extension_email}"  # Formatted username

    return username


def save_email(emails: str) -> None:
    """Save email in txt"""

    file_path: str = "src/data/emails.txt"

    with open(file_path, "a+") as data:
        data.write(emails)


def email_generator(amounts: int, password: str) -> str:
    """Generate bulk email."""

    for number_of_emails in range(1, amounts + 1):
        # Request body
        url: str = "https://api.mail.tm/accounts"
        headers: Mapping[str, str] = {
            "accept": "application/ld+json",
            "Content-Type": "application/ld+json",
        }
        username = username_generator()
        data: Mapping[str, str] = {
            "address": username,
            "password": password
        }

        if (platform.system()) == "Windows":
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

        email = asyncio.run(request_post(url, data, headers))  # Requests POST
        emails: str = f"{email['address']}|{password}\n"
        save_email(emails=emails)

        console.log(f"[green][b]:white_check_mark: Email created successfully {number_of_emails}[/][/]")


def main():
    ui.ascii()

    parser = ArgumentParser(prog="main.py", description="Bulk email generator")
    parser.add_argument(
        "-a",
        "--amounts",
        type=int,
        required=True,
        help="Desired amount of generated emails",
    )
    parser.add_argument(
        "-p",
        "--password",
        type=str,
        help="Email password",
        required=True,
    )
    args = parser.parse_args()

    try:
        if (args.amounts) > 100:
            console.print(":warning:[red][b]  [underline]It is not recommended to exceed 100 emails[/][/][/]")

            confirm_continuation = Prompt.ask("Do you want to continue?", choices=["y", "n"])
            if (confirm_continuation) == "y":
                pass

            elif (confirm_continuation) == "n":
                console.print("\n[red][b]:x: Leaving....[/][/]")
                exit()

        print("\n")
        with console.status("[green][b]:e-mail: Creating email...[/][/]") as _:
            email_generator(amounts=args.amounts, password=args.password)
            console.print("\n[cyan][b]:exclamation_mark: Emails saved in [underline]src/data/emails.txt[/][/][/]")

    # Except erros
    except KeyboardInterrupt:
        console.print("\n[red][b]:x: Leaving....[/][/]")

    except KeyError as error:
        console.print(f"\n[red][b]:x: ERROR: {error}[/][/]")

    except aiohttp.client_exceptions.ClientConnectorError as error:
        console.print(f"\n[red][b]:x: ERROR: {error}[/][/]")

    except aiohttp.client_exceptions.InvalidURL as error:
        console.print(f"\n[red][b]:x: ERROR: InvalidURL {error}[/][/]")


if __name__ == "__main__":
    main()
