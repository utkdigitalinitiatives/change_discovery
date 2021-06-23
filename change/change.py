import json
from math import ceil


class Collection:
    def __init__(self, items, items_per_page=100, base_url="https://example.com"):
        self.size = len(items)
        self.items_per_page = items_per_page
        self.items = items
        self.chunks = self.build_chunks()
        self.base = base_url
        self.id = f"{base_url}/activity/all-changes"
        self.last_page = self.__get_last_page()

    def __get_last_page(self):
        return ceil(self.size / self.items_per_page)

    def build_chunks(self):
        return [
            self.items[i * self.items_per_page : (i + 1) * self.items_per_page]
            for i in range(
                (len(self.items) + self.items_per_page - 1) // self.items_per_page
            )
        ]

    def generate_pages(self):
        i = 1
        is_last_page = False
        for chunk in self.chunks:
            if i == self.last_page:
                is_last_page = True
            PageOfChanges(page_number=i, pids=chunk, base_url=self.base, is_last_page=is_last_page).serialize()
            i += 1
        return

    def build(self):
        collection = {
            "@context": "http://iiif.io/api/discovery/1/context.json",
            "id": self.id,
            "type": "OrderedCollection",
            "totalItems": self.size,
            "first": {
                "id": f"{self.base}/activity/page-1",
                "type": "OrderedCollectionPage",
            },
            "last": {
                "id": f"{self.base}/activity/page-{self.last_page}",
                "type": "OrderedCollectionPage",
            },
        }
        return collection


class PageOfChanges:
    def __init__(self, page_number, pids, base_url, is_last_page=False):
        self.page_number = page_number
        self.pids = pids
        self.base_url = base_url
        self.is_last_page = is_last_page

    def get_activities(self):
        return [LevelZeroActivity(pid).build() for pid in self.pids]

    def build(self):
        page_of_changes = {
            "@context": "http://iiif.io/api/discovery/1/context.json",
            "id": f"{self.base_url}/activity/{self.page_number}",
            "type": "OrderedCollectionPage",
            "partOf": {
                "id": f"{self.base_url}/activity/all-changes",
                "type": "OrderedCollection",
            },
        }
        if self.page_number != 1:
            page_of_changes["prev"] = {
                "id": f"{self.base_url}/activity/page-{self.page_number-1}",
                "type": "OrderedCollectionPage",
            }
        if not self.is_last_page:
            page_of_changes["next"] = {
                "id": f"{self.base_url}/activity/page-{self.page_number+1}",
                "type": "OrderedCollectionPage",
            }
        page_of_changes["orderedItems"] = self.get_activities()
        return page_of_changes

    def serialize(self):
        with open(f"activity/page-{self.page_number}.json", "w") as page_activity:
            json.dump(self.build(), page_activity, indent=4)


class LevelZeroActivity:
    def __init__(self, pid):
        self.pid = pid

    @staticmethod
    def __format_pid(pid):
        return pid.replace(":", "/")

    def build(self):
        return {
            "type": "Update",
            "object": {
                "id": f"https://digital.lib.utk.edu/assemble/manifest/{self.__format_pid(self.pid)}",
                "type": "Manifest",
            },
        }


if __name__ == "__main__":
    x = Collection([])
    print(x.last_page)
