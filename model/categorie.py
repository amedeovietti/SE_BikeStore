from dataclasses import dataclass

@dataclass
class Categoria:
    id: int
    category_name: str

    def __str__(self):
        return self.category_name

    def __repr__(self):
        return self.category_name
