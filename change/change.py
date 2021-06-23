import json
from math import ceil


class Collection:
    def __init__(self, items, items_per_page=100, base_url="https://example.com"):
        self.size = len(items)
        self.items_per_page = items_per_page
        self.base = base_url
        self.id = f"{base_url}/activity/all-changes"
        self.last_page = self.__get_last_page()

    def __get_last_page(self):
        return ceil(self.size/self.items_per_page)

    def build(self):
        collection = {
            "@context": "http://iiif.io/api/discovery/1/context.json",
            "id": self.id,
            "type": "OrderedCollection",
            "totalItems": self.size,
            "first": {
                "id": f"{self.base}/activity/page-1",
                "type": "OrderedCollectionPage"
            },
            "last": {
                "id": f"{self.base}/activity/page-{self.last_page}",
                "type": "OrderedCollectionPage"
            }
        }

        return collection


class LevelZeroActivity:
    def __init__(self, pid):
        self.pid = pid

    @staticmethod
    def __format_pid(pid):
        return pid.replace(':', "/")

    def build(self):
        return {
            "type": "Update",
            "object": {
                "id": f"https://digital.lib.utk.edu/assemble/manifest/{self.__format_pid(self.pid)}",
                "type": "Manifest"
            }
        }


if __name__ == "__main__":
    x = Collection([])
    print(x.last_page)