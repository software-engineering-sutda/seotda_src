from typing import List

ranks = [
    {"name": "삼팔광땡", "condition": lambda c1, c2: [c1.month, c2.month] == [3,8] and c1.is_gwang and c2.is_gwang},
    {"name": "일팔광땡", "condition": lambda c1, c2: [c1.month, c2.month] == [1,8] and c1.is_gwang and c2.is_gwang},
    {"name": "일삼광땡", "condition": lambda c1, c2: [c1.month, c2.month] == [1,3] and c1.is_gwang and c2.is_gwang},
    
    {"name": "땡", "condition": lambda c1, c2: c1.month == c2.month},
    
    {"name": "알리", "condition": lambda c1, c2: [c1.month, c2.month] == [1, 2]},
    {"name": "독사", "condition": lambda c1, c2: [c1.month, c2.month] == [1, 4]},
    {"name": "구삥", "condition": lambda c1, c2: [c1.month, c2.month] == [1, 9]},
    {"name": "장삥", "condition": lambda c1, c2: [c1.month, c2.month] == [1, 10]},
    {"name": "장사", "condition": lambda c1, c2: [c1.month, c2.month] == [4, 10]},
    {"name": "세륙", "condition": lambda c1, c2: [c1.month, c2.month] == [4, 6]},
    
    {"name": "갑오", "condition": lambda c1, c2: (c1.month + c2.month) % 10 == 9},
    {"name": "망통", "condition": lambda c1, c2: (c1.month + c2.month) % 10 == 0},

    {"name": "땡잡이", "condition": lambda c1, c2: [c1.month, c2.month] == [3,7] and (c1.is_gwang and c2.is_yul)},
    {"name": "구사", "condition": lambda c1, c2: sorted([c1.month, c2.month]) == [4, 9] and (c1.is_yul and c2.is_yul)},
    {"name": "멍텅구리 구사", "condition": lambda c1, c2: c1.month == 4 and c1.is_yul and c2.month == 9 and c2.is_yul or c2.month == 4 and c2.is_yul and c1.month == 9 and c1.is_yul},
    {"name": "암행어사", "condition": lambda c1, c2: [c1.month, c2.month] == [4,7] and (c1.is_yul and c2.is_yul)},
]

class GameRoom:
    def __init__(self, room_name: str,  jokbo : list, max_players: int = 4,):
        self.room_name: str = room_name
        self.max_players: int = max_players
        self.players: List[Player] = []
        self.deck: Deck = Deck()
        self.started: bool = False
        self.jokbo = jokbo

    def add_player(self, player: Player) -> None:
        if len(self.players) >= self.max_players:
            raise Exception("플레이어 수 초과")
        self.players.append(player)

    def start_game(self) -> None:
        if len(self.players) < 4:
            raise Exception("플레이어가 부족합니다.")
        self.deck.reset()
        self.deck.shuffle()
        # 플레이어 카드 분배 (한장씩 두바퀴)
        for i in range(2):
            for player in self.players:
                player.receive_card(self.deck.draw())
        # 플레이어 카드 month를 기준으로 정렬
        for player in self.players:
            player.hand.sort(key=lambda card: card.month)
        self.started = True

    def calculate_scores(self) -> None:
        for player in self.players:
            for idx, hand in enumerate(self.jokbo) :
                if hand['condition'](player.hand[0], player.hand[1]):
                    if hand['name'] == "땡" :
                        player.score = {f"{player.hand[0].month}땡": player.hand[0].month}
                    else :
                        player.score = {hand['name']: idx+1}
            if not player.score : # 족보에 속하지 않는 경우 (n끗)
                player.score = {f"{(player.hand[0].month + player.hand[1].month) % 10}끗" : (player.hand[0].month + player.hand[1].month)} 
        
        return {player.name: player.score for player in self.players}
    
    def get_winner(self) -> Optional[Player]:
        self.calculate_scores()
        sorted_players = sorted(
            [p for p in self.players if p.score is not None],
            key=lambda p: p.score,
            reverse=True
        )
        if sorted_players :
            return [hand.show() for hand in sorted_players[0].hand]

    def reset_game(self) -> None:
        self.deck.reset()
        for player in self.players:
            player.reset()
        self.started = False

    def show_all_hands(self):
        return {player.name: [card.show() for card in player.hand] for player in self.players}