import random
from typing import List, Iterator, Callable, Tuple

class Deck:
    def __init__(self):
        self.init_deck()

    def __iter__(self) -> Iterator[Card]:
        return iter(self.deck)
        
    def __len__(self) -> int:
        return len(self.deck)
        
    def show(self) -> List[str]:
        return [i.show() for i in self.deck]

    def init_deck(self) -> List[Card]:
        self.deck : List[Card] = [
            Card(1, is_gwang=True), Card(1, is_yul = True), Card(1), Card(1), 
            Card(2, is_yul = True), Card(2), Card(2), Card(2),
            Card(3, is_gwang=True), Card(3), Card(3), Card(3),
            Card(4, is_yul = True), Card(4), Card(4), Card(4),
            Card(5, is_yul = True), Card(5), Card(5), Card(5),
            Card(6, is_yul=True), Card(6), Card(6), Card(6),
            Card(7, is_yul=True), Card(7), Card(7), Card(7),
            Card(8, is_gwang=True), Card(8, is_yul = True), Card(8), Card(8),
            Card(9, is_yul=True), Card(9), Card(9), Card(9),
            Card(10, is_yul=True), Card(10), Card(10), Card(10)
        ]
        return self.deck

    def reset(self):
        self.deck = self.init_deck()

    def shuffle(self) -> None:
        random.shuffle(self.deck)

    def draw(self, n : int = 1) -> List[Card]:
        """카드중 하나를 비복원 추출"""
        if n > len(self.deck):
            raise ValueError("덱에 카드가 부족합니다.")
        drawn = self.deck[:n]
        self.deck = self.deck[n:]
        return drawn
