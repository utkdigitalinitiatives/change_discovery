from data.audio import audio
from data.books import books
from data.large import large_images
from data.video import video
from change.change import Collection


def get_all():
    all = []
    for item in large_images:
        all.append(item)
    for item in audio:
        all.append(item)
    for item in video:
        all.append(item)
    for item in books:
        all.append(item)
    return all


if __name__ == "__main__":
    x = Collection(get_all(), base_url="https://utkdigitalinitiatives.github.io/change_discovery")
    all_chunks = x.generate_pages()
