import random
import numpy as np


class Player:
    def __init__(self, index):
        self.index = index
        self.hand = []
        self.discarded = []
        self.out = False

    def draw(self, tile):
        self.hand.append(tile)

    def discard(self, tile):
        self.hand.remove(tile)
        self.discarded.append(tile)

    def out(self):
        if is_out(self.hand):
            self.out = True


# 最初に麻雀牌をシャッフルする
def initialize_tiles(tiles):
    random.shuffle(tiles)
    return tiles


# 麻雀牌を配る
def draw_tiles(tiles, player, is_initial=False):
    if is_initial:
        for _ in range(5):
            player.draw(tiles.pop(0))
    else:
        if len(tiles) == 0:
            return tiles
        player.draw(tiles.pop(0))
    return tiles


def to_ternary(x):
    arr = []
    tmp = x
    for _ in range(4):
        arr.append(tmp % 3)
        tmp //= 3

    return np.array(arr)


# セットかどうかを判定する
def is_set(a, b, c):
    a = to_ternary(a)
    b = to_ternary(b)
    c = to_ternary(c)
    return np.sum((a + b + c) % 3) == 0


# 上がり判定
def is_out(player):
    hand = player.hand
    if len(hand) != 6:
        raise ValueError(f"Error!: 手牌の枚数が{len(hand)}枚です")
    for i in range(len(hand)):
        for j in range(i + 1, len(hand)):
            for k in range(j + 1, len(hand)):
                rest_ids = []
                for l in range(6):
                    if l not in {i, j, k}:
                        rest_ids.append(l)
            
                if is_set(hand[i], hand[j], hand[k]) and is_set(
                    hand[rest_ids[0]], hand[rest_ids[1]], hand[rest_ids[2]]
                ):
                    return True
    return False


TILES = list(range(81))
PLAYERS = [Player(i) for i in range(4)]


def main():
    tiles = initialize_tiles(TILES)
    undrawned_tiles = [tiles.pop(0)]
    print(f"ドラ表示牌: {undrawned_tiles}")

    for player in PLAYERS:
        tiles = draw_tiles(tiles, player, is_initial=True)
    for player in PLAYERS:
        print(f"=================Player: {player.index}=================")
        print(player.hand)
        print(player.discarded)
    while True:
        if len(tiles) == 0:
            print("不聴!")
            break
        print()
        print("次のターンです")
        print()
        for player in PLAYERS:
            tiles = draw_tiles(tiles, player)
            if len(tiles) == 0:
                print("No more tiles!")
                break
            if is_out(player):
                print(f"Player: {player.index} is out!")
                return
            discarded_tile = random.choice(player.hand)
            player.discard(discarded_tile)
            print(f"=================Player: {player.index}=================")
            print(player.hand)
            print(player.discarded)
            


if __name__ == "__main__":
    main()
