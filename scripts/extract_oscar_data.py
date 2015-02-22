import json
import sys
import urllib

from bs4 import BeautifulSoup


PREFIX = "oscar2015mp1"
POINTS = {
    "best-picture": 8,
    "directing": 5,
    "actor-in-a-leading-role": 5,
    "actress-in-a-leading-role": 5,
    "animated-feature-film": 5,
    "documentary-feature": 5,
    "foreign-language-film": 4,
    "writing-original-screenplay": 4,
    "writing-adapted-screenplay": 4,
    "actor-in-a-supporting-role": 4,
    "actress-in-a-supporting-role": 4,
    "film-editing": 3,
    "cinematography": 3,
    "music-original-song": 3,
    "music-original-score": 3,
    "short-film-animated": 3,
    "short-film-live-action": 3,
    "costume-design": 2,
    "production-design": 2,
    "documentary-short-subject": 2,
    "makeup-and-hairstyling": 2,
    "sound-editing": 2,
    "sound-mixing": 2,
    "visual-effects": 2
}


def parse_nominee(element):
    url = element.attrs["href"]
    text = element.get_text()
    category, nominee = [
        p for p in url.split("/nominees", 1)[1].split("/") if p]
    image_key = "{0}-{1}-{2}".format(PREFIX, category, nominee)

    information = {
        "key": nominee,
        "image": image_key,
        "category": category,
        "category_name": text
    }

    return information


def main():
    url = sys.argv[1]
    body = urllib.urlopen(url).read()
    soup = BeautifulSoup(body)

    images = {}
    titles = {}
    subtitles = {}

    for li in soup.find_all("li"):
        if "data-img" not in li.attrs:
            continue

        image_key = li.attrs["data-img"]

        for image_el in li.find_all("img"):
            images[image_key] = image_el.attrs["src"]
            break

        for title_el in li.select("span.title"):
            titles[image_key] = title_el.get_text()
            break

        for subtitle_el in li.select("span.subtitle"):
            subtitles[image_key] = subtitle_el.get_text()
            break

    categories = {}

    for element in soup.select("li.film.contentArea"):
        image_elements = element.find_all("img")
        image_url = ""
        if len(image_elements):
            image_url = image_elements[0].attrs["src"]

        title = element.select("span.title")[0].get_text()
        nominations_ul = element.find_all("ul", class_="nominations")[0]
        nominations_elements = nominations_ul.find_all("a")
        nominations = [
            parse_nominee(e) for e in nominations_elements
        ]

        for nominee in nominations:
            nominee["title"] = titles.get(nominee["image"], title)
            nominee["subtitle"] = subtitles.get(nominee["image"], "")
            nominee["image_url"] = images.get(nominee["image"], image_url)
            category_name = nominee.pop("category_name")
            category_key = nominee.pop("category")

            category = categories.setdefault(category_key, {
                "key": category_key,
                "title": category_name,
                "nominees": []
            })

            category["nominees"].append(nominee)

    print json.dumps({
        "categories": categories.values(),
        "points": POINTS
    }, indent=2, separators=(',', ': '), sort_keys=True)


if __name__ == "__main__":
    main()
