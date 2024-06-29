import requests
import json
import os
from bs4 import BeautifulSoup, Tag
from dataclasses import dataclass
from argparse import ArgumentParser

URL = "https://free-proxy-list.net/"
FREE_PROXIES_TABLE_ROWS_SELECTOR = ".fpl-list > table > tbody > tr"


@dataclass(frozen=True, repr=True)
class Proxy:
    address: str
    port: int
    country: str
    anonymity: str
    is_google: bool
    is_https: bool

    def is_anonymous(self) -> bool:
        return self.anonymity == "anonymous"


def get_all_proxies() -> list[dict]:
    page = BeautifulSoup(requests.get(URL).text, features="html.parser")
    proxies_rows: list[list[Tag]] = [
        list(row.children) for row in page.select(FREE_PROXIES_TABLE_ROWS_SELECTOR)
    ]

    return [
        Proxy(
            row[0].text,
            int(row[1].text),
            row[3].text,
            row[4].text,
            row[5].text == "yes",
            row[6].text == "yes",
        )
        for row in proxies_rows
    ]


def to_json(proxies: list[Proxy]):
    return json.dumps([vars(proxy) for proxy in proxies], ensure_ascii=False)


def main(args):
    proxies = to_json(get_all_proxies())

    if args.output:
        with open(args.output, "w") as output:
            output.write(proxies)
    else:
        print(proxies)


if __name__ == "__main__":
    parser = ArgumentParser(
        prog=os.path.basename(__file__),
        description="Get currently available free proxies from free-proxy-list.net",
    )

    parser.add_argument("--output", help="specify output file")

    main(parser.parse_args())
