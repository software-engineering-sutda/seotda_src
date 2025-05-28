import random

class Card: 
    def __init__(self, month : int, is_gwang : bool = False, is_yul : bool = False) :
        self.month: int = month
        self.is_gwang: bool = is_gwang
        self.is_yul: bool = is_yul
        
    def show(self) -> str:
        flag = "Normal"
        if self.is_gwang :
            flag = "Gwang"
        elif self.is_yul :
            flag = "Yul"
        if flag != "Normal" :
            return f"{self.month}월{flag}"
        else :
            return f"{self.month}월"
