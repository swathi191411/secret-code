from html.parser import HTMLParser
from urllib.request import Request, urlopen


class TableParser(HTMLParser):
    """Collects the text of every table row in the page as a list of cells."""

    def __init__(self):
        super().__init__()
        self.rows, self.row, self.cell, self.in_cell = [], [], "", False

    def handle_starttag(self, tag, attrs):
        if tag == "tr":
            self.row = []
        elif tag in ("td", "th"):
            self.in_cell, self.cell = True, ""

    def handle_endtag(self, tag):
        if tag in ("td", "th"):
            self.in_cell = False
            self.row.append(self.cell.strip())
        elif tag == "tr" and self.row:
            self.rows.append(self.row)

    def handle_data(self, data):
        if self.in_cell:
            self.cell += data


def decode_secret_message(url: str) -> None:
    req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    page = urlopen(req).read().decode("utf-8")

    parser = TableParser()
    parser.feed(page)

    points = []
    for row in parser.rows:
        if len(row) == 3 and row[0].isdigit() and row[2].isdigit():
            points.append((int(row[0]), row[1], int(row[2])))

    width = max(x for x, _, _ in points) + 1
    height = max(y for _, _, y in points) + 1
    grid = [[" "] * width for _ in range(height)]
    for x, char, y in points:
        grid[y][x] = char  # y = 0 is the top row

    print("\n".join("".join(row) for row in grid))


if __name__ == "__main__":
    decode_secret_message(
        "https://docs.google.com/document/d/e/2PACX-1vSvM5gDlNvt7npYHhp_XfsJvuntUhq184By5xO_pA4b_gCWeXb6dM6ZxwN8rE6S4ghUsCj2VKR21oEP/pub"
    )
