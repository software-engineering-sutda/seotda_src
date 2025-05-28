import random
from typing import List, Iterator, Callable, Tuple

class Card: 
    def __init__(self, month : int, is_gwang : bool = False, is_yul : bool = False) :
        self.month = month
        self.is_gwang = is_gwang
        self.is_yul = is_yul
        
    def show(self) -> str:
        if self.is_gwang:
            return f"{self.month}월 Gwang"
        if self.is_yul:
            return f"{self.month}월 Yul"
        return f"{self.month}월"
