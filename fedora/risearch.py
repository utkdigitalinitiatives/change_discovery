import requests


class ResourceIndexSearch:
    def __init__(self, risearch_endpoint="http://localhost:8080/fedora/risearch"):
        self.risearch_endpoint = risearch_endpoint

    @staticmethod
    def escape_query(query):
        return (
            query.replace("*", "%2A")
            .replace(" ", "%20")
            .replace("<", "%3C")
            .replace(":", "%3A")
            .replace(">", "%3E")
            .replace("#", "%23")
            .replace("\n", "")
            .replace("?", "%3F")
            .replace("{", "%7B")
            .replace("}", "%7D")
            .replace("/", "%2F")
        )

    def validate_language(self, language):
        if language in self.valid_languages:
            return language
        else:
            raise Exception(
                f"Supplied language is not valid: {language}. Must be one of {self.valid_languages}."
            )

    def validate_format(self, user_format):
        if user_format in self.valid_formats:
            return user_format
        else:
            raise Exception(
                f"Supplied format is not valid: {user_format}. Must be one of {self.valid_formats}."
            )


class TuplesSearch(ResourceIndexSearch):
    def __init__(
        self,
        language="sparql",
        riformat="CSV",
        ri_endpoint="http://localhost:8080/fedora/risearch",
    ):
        super().__init__(ri_endpoint)
        ResourceIndexSearch.__init__(self)
        self.valid_languages = ("itql", "sparql")
        self.valid_formats = ("CSV", "Simple", "Sparql", "TSV")
        self.language = self.validate_language(language)
        self.format = self.validate_format(riformat)
        self.base_url = (
            f"{self.risearch_endpoint}?type=tuples"
            f"&lang={self.language}&format={self.format}"
        )

    def get_large_images_by_collection(self, collection):
        sparql_query = self.escape_query(
            f"PREFIX fedora-model: <info:fedora/fedora-system:def/model#> PREFIX fedora-rels-ext: "
            f"<info:fedora/fedora-system:def/relations-external#> PREFIX isl-rels-ext: "
            f"<http://islandora.ca/ontology/relsext#> SELECT $pid FROM <#ri> WHERE {{ $pid "
            f"fedora-model:hasModel <info:fedora/islandora:sp_large_image_cmodel>;"
            f"fedora-rels-ext:isMemberOfCollection <info:fedora/{collection}> . }}"
        )
        results = requests.get(f"{self.base_url}&query={sparql_query}").content.decode("utf-8").split("\n")
        return [result.replace('info:fedora/', '') for result in results if ":" in result]

    def get_all_large_images(self):
        sparql_query = self.escape_query(
            f"PREFIX fedora-model: <info:fedora/fedora-system:def/model#> PREFIX fedora-rels-ext: "
            f"<info:fedora/fedora-system:def/relations-external#> PREFIX isl-rels-ext: "
            f"<http://islandora.ca/ontology/relsext#> SELECT $pid FROM <#ri> WHERE {{ $pid "
            f"fedora-model:hasModel <info:fedora/islandora:sp_large_image_cmodel> .}}"
        )
        results = requests.get(f"{self.base_url}&query={sparql_query}").content.decode("utf-8").split("\n")
        return [result.replace('info:fedora/', '') for result in results if ":" in result]

    def get_books(self):
        sparql_query = self.escape_query(
            f"PREFIX fedora-model: <info:fedora/fedora-system:def/model#> PREFIX fedora-rels-ext: "
            f"<info:fedora/fedora-system:def/relations-external#> PREFIX isl-rels-ext: "
            f"<http://islandora.ca/ontology/relsext#> SELECT $pid FROM <#ri> WHERE {{ $pid "
            f"fedora-model:hasModel <info:fedora/islandora:bookCModel> . }}"
        )
        results = requests.get(f"{self.base_url}&query={sparql_query}").content.decode("utf-8").split("\n")
        return [result.replace('info:fedora/', '') for result in results if ":" in result]

    def get_audio(self):
        sparql_query = self.escape_query(
            f"PREFIX fedora-model: <info:fedora/fedora-system:def/model#> PREFIX fedora-rels-ext: "
            f"<info:fedora/fedora-system:def/relations-external#> PREFIX isl-rels-ext: "
            f"<http://islandora.ca/ontology/relsext#> SELECT $pid FROM <#ri> WHERE {{ $pid "
            f"fedora-model:hasModel <info:fedora/islandora:sp-audioCModel> . }}"
        )
        results = requests.get(f"{self.base_url}&query={sparql_query}").content.decode("utf-8").split("\n")
        return [result.replace('info:fedora/', '') for result in results if ":" in result]

    def get_video(self):
        sparql_query = self.escape_query(
            f"PREFIX fedora-model: <info:fedora/fedora-system:def/model#> PREFIX fedora-rels-ext: "
            f"<info:fedora/fedora-system:def/relations-external#> PREFIX isl-rels-ext: "
            f"<http://islandora.ca/ontology/relsext#> SELECT $pid FROM <#ri> WHERE {{ $pid "
            f"fedora-model:hasModel <info:fedora/islandora:sp_videoCModel> . }}"
        )
        results = requests.get(f"{self.base_url}&query={sparql_query}").content.decode("utf-8").split("\n")
        return [result.replace('info:fedora/', '') for result in results if ":" in result]


if __name__ == "__main__":
    x = TuplesSearch(language="sparql").get_all_large_images()
    print(x)
