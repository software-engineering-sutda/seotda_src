import random
from typing import List, Iterator, Callable, Tuple

jokbo = [
    {"name": "암행어사", "condition": lambda c1, c2: [c1.month, c2.month] == [4,7] and (c1.is_yul and c2.is_yul), "score" : 1},
    {"name": "땡잡이", "condition": lambda c1, c2: [c1.month, c2.month] == [3,7] and (c1.is_gwang and c2.is_yul), "score" : 0}, # +110
    {"name": "멍텅구리 구사", "condition": lambda c1, c2: [c1.month, c2.month] == [4, 9] and (c1.is_yul and c2.is_yul), "score" : 3}, # 구땡이하 재경기 +110
    {"name": "구사", "condition": lambda c1, c2: [c1.month, c2.month] == [4, 9] and not(c1.is_yul and c2.is_yul), "score" : 3}, # 알리 이하 재시작
    
    {"name": "망통", "condition": lambda c1, c2: (c1.month + c2.month) % 10 == 0, "score" : 0},
    {"name": "갑오", "condition": lambda c1, c2: (c1.month + c2.month) % 10 == 9, "score" : 9},
    {"name": "세륙", "condition": lambda c1, c2: [c1.month, c2.month] == [4, 6], "score" : 10},
    {"name": "장사", "condition": lambda c1, c2: [c1.month, c2.month] == [4, 10], "score" : 11},
    {"name": "장삥", "condition": lambda c1, c2: [c1.month, c2.month] == [1, 10], "score" : 12},
    {"name": "구삥", "condition": lambda c1, c2: [c1.month, c2.month] == [1, 9], "score" : 13},
    {"name": "독사", "condition": lambda c1, c2: [c1.month, c2.month] == [1, 4], "score" : 14},
    {"name": "알리", "condition": lambda c1, c2: [c1.month, c2.month] == [1, 2], "score" : 15},
    
    {"name": "땡", "condition": lambda c1, c2: c1.month == c2.month, "score" : 100}, # 장땡 구현하기
    
    {"name": "일삼광땡", "condition": lambda c1, c2: [c1.month, c2.month] == [1,3] and c1.is_gwang and c2.is_gwang, "score" : 1000},
    {"name": "일팔광땡", "condition": lambda c1, c2: [c1.month, c2.month] == [1,8] and c1.is_gwang and c2.is_gwang, "score" : 1100},
    {"name": "삼팔광땡", "condition": lambda c1, c2: [c1.month, c2.month] == [3,8] and c1.is_gwang and c2.is_gwang, "score" : 1300},
]

class GameRoom:
    def __init__(self, room_name: str,  jokbo : list, max_players: int = 4):
        self.room_name: str = room_name
        self.max_players: int = max_players
        self.players: List[Player] = []
        self.deck = Deck()
        self.started: bool = False
        self.jokbo = jokbo

    def add_player(self, player: Player) -> None:
        if len(self.players) >= self.max_players:
            raise Exception("플레이어 수 초과")
        self.players.append(player)

    def start_game(self, is_regame = False, is_test = False) -> None:
        self.deck.reset()
        self.deck.shuffle()
        if is_test :
            pass  
        elif is_regame:
            for i in range(2): # 플레이어 카드 분배 (한장씩 두바퀴)
                for player in self.players:
                    player.receive_card(self.deck.draw()) 
        else :
            if len(self.players) < 4:
                raise Exception("플레이어가 부족합니다.")
            for i in range(2): # 플레이어 카드 분배 (한장씩 두바퀴)
                for player in self.players:
                    player.receive_card(self.deck.draw())
        self.started = True     
        self.calculate()   
        return self.show_all_result(), self.get_winner()
                
    def calculate(self) -> None:   
        for player in self.players:
            player.result = None 
            player.hand.sort(key=lambda card: card.month)      
            # 땡, 광땡, 중간족보, 특수족보
            for idx, hand in enumerate(self.jokbo) :
                if hand['condition'](player.hand[0], player.hand[1]):
                    if hand['name'] == "땡" :
                        if (player.hand[0].month + player.hand[0].month) == 20 :
                            player.result = ["장땡", player.hand[0].month + hand['score']]
                        else :
                            player.result = ["땡", player.hand[0].month + hand['score']]
                    else :
                        player.result = [hand['name'], hand['score']]
                        
            # 족보에 속하지 않는 경우 : n끗
            if not player.result : 
                player.result = ["끗", (player.hand[0].month + player.hand[1].month) % 10]
                
            # 어떤 족보에도 속하지 않는경우
            elif not player.result :
                raise Exception("점수계산에 오류가 발생했습니다")

    def get_winner(self):
        player_result = [p.result[0] for p in self.players]
        sorted_players = sorted( self.players, key=lambda p: p.result[1], reverse=True)
        
        if "암행어사" in player_result and set(player_result) & set(["일삼광땡", "일팔광땡"]):
            plyers[player_result.index("암행어사")].result[1] == 1200
                    
        if "땡잡이" in player_result and player_result in "땡" :
            plyers[player_result.index("땡잡이")].result[1] == 110

        if "멍텅구리 구사" in player_result and sorted_players[0].result[1] <= 1200 :
            return self.start_game(is_regame=True)
            
        if "구사" in player_result and sorted_players[0].result[1] <= 15 :
            return self.start_game(is_regame=True)

        # 특수 규칙 계산 이후 다시 정렬
        sorted_players = sorted(
            self.players,
            key=lambda p: p.result[1],
            reverse=True
        )
        
        # 동점 발생시 게임 재시작
        winner = sorted_players[0]
        regame_player = [winner]
        for p in sorted_players[1:]:
            if winner.result[1] == p.result[1] :
                regame_player.append(p)

        if len(regame_player) > 1 :
            self.players = regame_player
            return self.start_game(is_regame=True)
   
        else : 
            return f"{winner.name} 우승"

    def reset_all_game(self) -> None:
        self.deck.reset()
        for player in self.players:
            player.reset()
        self.started = False
    
    def show_all_hands(self):
        return {player.name: [card.show() for card in player.hand] for player in self.players}

    def show_all_result(self):
        return {player.name: player.result for player in self.players}   
