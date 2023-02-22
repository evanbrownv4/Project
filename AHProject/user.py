from dataclasses import dataclass

@dataclass
class User:
    user_id: int
    username: str
    password: str
    score: int

    def __str__(self):
        return f"{self.fusername}'s score: {self.score}"