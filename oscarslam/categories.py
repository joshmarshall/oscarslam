import json

from oscarslam import config


class _Contest(object):

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


class Categories(object):

    def __init__(self):
        self.contests = {}
        for contest_id, path in config.CONTESTS.items():
            with open(path) as contest_fp:
                contest_data = json.loads(contest_fp.read())
                categories = contest_data["categories"]
                points = contest_data["points"]
                contest = _Contest(categories, points)
                self.contests[contest_id] = contest

    def contest(self, contest_id):
        return self.contests[contest_id]


CATEGORIES = Categories()
