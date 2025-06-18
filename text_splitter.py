from typing import List

class TextSplitter:
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        if chunk_overlap >= chunk_size:
            raise ValueError("chunk_overlap must be less than chunk_size")
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def split_text(self, text: str) -> List[str]:
        raise NotImplementedError

    def merge_splits(self, splits: List[str], separator: str) -> List[str]:
        docs = []
        current_doc = []
        total = 0

        for chunk in splits:
            chunk_len = len(chunk)
            if total + chunk_len >= self.chunk_size:
                if current_doc:
                    docs.append(separator.join(current_doc).strip())
                while total > self.chunk_overlap and current_doc:
                    total -= len(current_doc[0])
                    current_doc.pop(0)
            current_doc.append(chunk)
            total += chunk_len

        if current_doc:
            docs.append(separator.join(current_doc).strip())

        return docs


class RecursiveCharacterTextSplitter(TextSplitter):
    def __init__(self, chunk_size=1000, chunk_overlap=200, separators=None):
        super().__init__(chunk_size, chunk_overlap)
        self.separators = separators or ["\n\n", "\n", ".", ",", " ", ""]

    def split_text(self, text: str) -> List[str]:
        for separator in self.separators:
            if separator and separator in text:
                splits = text.split(separator)
                chunks = []
                for s in splits:
                    if len(s) < self.chunk_size:
                        chunks.append(s)
                    else:
                        chunks += self.split_text(s)
                return self.merge_splits(chunks, separator)

        return [text]
