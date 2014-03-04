import json
import os
import oscarslam.config


class _Categories(object):

    def __init__(self, categories, points):
        self._categories = dict([(v["key"], v) for v in categories])
        self._points = points
        self._ordered_points = [k for k in points]
        self._ordered_points.sort(key=lambda x: self._points[x], reverse=True)

    def __iter__(self):
        for key in self._ordered_points:
            yield self.get(key)

    def __getitem__(self, index):
        key = self._ordered_points[index]
        return self.get(key)

    def get(self, key):
        points = self._points[key]
        category = self._categories[key]
        return _Category(category, points)

    def __len__(self):
        return len(self._categories)


class _Category(object):

    def __init__(self, category, points):
        self._category = category
        for attribute in category:
            setattr(self, attribute, category[attribute])
        self.points = points
        self.nominees = _Nominees(category["nominees"])


class _Nominees(object):

    def __init__(self, nominees):
        self._nominees = nominees

    def __iter__(self):
        for nominee in self._nominees:
            yield _Nominee(nominee)

    def __getitem__(self, key):
        return _Nominee(self._nominees[key])

    def __len__(self):
        return len(self._nominees)

    def get(self, key):
        for nominee in self:
            if nominee.key == key:
                return nominee
        return None


class _Nominee(object):

    def __init__(self, nominee):
        self._nominee = nominee
        self.key = nominee["key"]
        self.title = nominee["title"]
        self.subtitle = nominee.get("subtitle")

    def image_url(self, width=None, height=None):
        return self._nominee["image_url"]


CATEGORIES = []


if os.path.exists(oscarslam.config.CATEGORIES_PATH):
    with open(oscarslam.config.CATEGORIES_PATH) as categories_fp:
        CATEGORIES = json.loads(categories_fp.read())


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


CATEGORIES = _Categories(CATEGORIES, POINTS)
