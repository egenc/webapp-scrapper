"""Class for techfinder functionality"""
from dataclasses import dataclass, field
import nltk
from nltk.corpus import stopwords

@dataclass
class TechFinder():
    """input: source path for txt
       purposed for detecting tech stack from job description
    """
    nltk.download("stopwords")
    stopwords: list[str] = field(default_factory=lambda: stopwords.words("english"))
    path: str = "tech_stack.txt"

    def read_txt(self, path):
        """reading txt file content"""
        with open(path, encoding="utf-8") as source:
            txt = source.read()
        return txt

    def tech_stack_finder(self, job_desc):
        """detecting techs from text"""
        tech_stack = []

        source_txt = self.read_txt(self.path).split("\n")
        for ele in job_desc.split(" "):
            if ele.lower() in source_txt and ele.lower() not in self.stopwords:
                tech_stack.append(ele)
        return list(set(tech_stack))
