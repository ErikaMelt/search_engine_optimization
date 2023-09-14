class EvaluationData:
    def __init__(
        self,
        query_id,
        title,
        url,
        snippet,
        search_engine,
        scraping_id,
        intent_desc,
        position,
        id,
    ):
        self.query_id = query_id
        self.intent_desc = intent_desc
        self.title = title
        self.url = url
        self.snippet = snippet
        self.search_engine = search_engine
        self.scraping_id = scraping_id
        self.position = position
        self.id = id

    def as_dict(self):
        return {
            "query_id": self.query_id,
            "intent_desc": self.intent_desc,
            "title": self.title,
            "url": self.url,
            "snippet": self.snippet,
            "search_engine": self.search_engine,
            "scraping_id": self.scraping_id,
            "position": self.position,
            "id": self.id,
        }
