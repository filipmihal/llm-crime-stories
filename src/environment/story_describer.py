from typing import List, Optional

from rake_nltk import Rake


class StoryDescriber:
    def __init__(self, n_descriptive: int):
        self._r = Rake()
        self._n_descriptive = n_descriptive

    def describe(self, story: str, n_descriptive: Optional[int] = None) -> List[str]:
        n_descriptive = n_descriptive or self._n_descriptive

        self._r.extract_keywords_from_text(story)
        keywords = self._r.get_ranked_phrases()

        return keywords if len(keywords) < n_descriptive else keywords[:n_descriptive]
