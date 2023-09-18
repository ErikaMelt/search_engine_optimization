import re
import spacy

nlp = spacy.load("en_core_web_sm")


def clean_text(search_results):
    for result in search_results:

        title = result.title
        snippet = result.snippet

        title = re.sub(r"[^a-zA-Z0-9\s-]", "", title)
        snippet = re.sub(r"[^a-zA-Z0-9\s-]", "", snippet)

        title = title.lower()
        snippet = snippet.lower()

        title_doc = nlp(title)
        snippet_doc = nlp(snippet)

        cleaned_title = " ".join(
            [token.lemma_ for token in title_doc if not token.is_stop]
        )
        cleaned_snippet = " ".join(
            [token.lemma_ for token in snippet_doc if not token.is_stop]
        )

        result.title = cleaned_title
        result.snippet = cleaned_snippet

    return search_results
