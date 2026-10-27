from html.parser import HTMLParser
import heapq
import re
import sys


class ProductParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.products = []

        self.current = None
        self.tag_stack = []
        self.capture = None
        self.text = ""

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        # attrs.get may return None if the attribute is present without a value.
        # Ensure we convert None to empty string before calling lower().
        classes = (attrs.get("class") or "").lower()

        # Start of a product
        if "product" in classes:
            self.current = {
                "name": "",
                "price": None,
                "rating": None
            }

        if self.current is None:
            return

        if "product-name" in classes or classes == "name":
            self.capture = "name"
            self.text = ""

        elif "price" in classes:
            self.capture = "price"
            self.text = ""

        elif "rating" in classes:
            self.capture = "rating"
            self.text = ""

        self.tag_stack.append(tag)

    def handle_data(self, data):
        if self.current is not None and self.capture:
            self.text += data.strip() + " "

    def handle_endtag(self, tag):
        if self.current is None:
            return

        if self.capture:
            value = self.text.strip()

            if self.capture == "name":
                self.current["name"] = value

            elif self.capture == "price":
                self.current["price"] = normalize_price(value)

            elif self.capture == "rating":
                self.current["rating"] = extract_rating(value)

            self.capture = None
            self.text = ""

        # Product block ended
        if tag in ("div", "article", "li"):
            if (
                self.current["name"]
                and self.current["price"] is not None
                and self.current["rating"] is not None
            ):
                self.products.append(self.current)
                self.current = None


def normalize_price(value):
    """
    Converts prices such as:
    $1,299.50 -> 1299.50
    ₹799      -> 799
    Rs. 499   -> 499
    """
    value = value.replace(",", "")

    match = re.search(r"\d+(?:\.\d+)?", value)

    if not match:
        return None

    number = float(match.group())

    if number.is_integer():
        return int(number)

    return number


def extract_rating(value):
    match = re.search(r"\d+(?:\.\d+)?", value)

    if not match:
        return None

    return float(match.group())


def read_file(filename):
    parser = ProductParser()

    with open(
        filename,
        "r",
        encoding="utf-8",
        errors="ignore"
    ) as file:

        for chunk in iter(lambda: file.read(1024 * 1024), ""):
            parser.feed(chunk)

    return parser.products


def main():
    input = sys.stdin.readline

    p, k = map(int, input().split())

    # name -> (price, rating)
    products = {}

    for _ in range(p):
        filename = input().strip()

        for product in read_file(filename):

            name = product["name"]
            price = product["price"]
            rating = product["rating"]

            # Remove duplicates by product name.
            # Keep the version with better rating.
            # If rating is same, keep lower price.
            if name not in products:
                products[name] = (price, rating)

            else:
                old_price, old_rating = products[name]

                if (
                    rating > old_rating
                    or
                    (
                        rating == old_rating
                        and price < old_price
                    )
                ):
                    products[name] = (price, rating)

    # Highest rating
    # Lower price
    # Lexicographically smaller name
    ranked = []

    for name, (price, rating) in products.items():
        ranked.append((name, price, rating))

    ranked.sort(
        key=lambda x: (
            -x[2],
            x[1],
            x[0]
        )
    )

    for name, price, rating in ranked[:k]:
        print(name, price, rating)


if __name__ == "__main__":
    main()