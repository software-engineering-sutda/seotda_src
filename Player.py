from typing import List
import Card

class Player:
    def __init__(self, name: str):
        self.name: str = name
        self.hand: List[Card] = []  # 두 장의 카드
        self.is_ready: bool = False
        self.result = None
        self.score = None  # 족보 점수 (비교용)

    def __repr__(self) -> str:
        return f"<Player {self.name}, Hand: {self.hand}>"

    def receive_card(self, cards: Card) -> None:
        # 카드 2장을 받는다.
        if len(self.hand) == 2 :
            self.hand: List[Card] = []
            self.hand.extend(cards)
        else :
            self.hand.extend(cards)

    def reset(self) -> None:
        # 새 라운드를 위한 초기화
        self.hand.clear()
        self.result = ('', 0)
        self.is_ready = False
        self.score = None
