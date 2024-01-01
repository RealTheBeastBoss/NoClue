from game import *

VALUE_TO_IMAGE = {
    2: DICE_TWO,
    3: DICE_THREE,
    4: DICE_FOUR,
    5: DICE_FIVE,
    6: DICE_SIX
}

class Dice:
    def __init__(self):
        self.value = 6

    def draw(self, pos):
        if self.value == 1:
            if Game.CLUE_CARDS_ACTIVE and len(Game.CLUE_CARD_DECK) > 0:
                dice_image = DICE_CLUE
            else:
                dice_image = DICE_ONE
        else:
            dice_image = VALUE_TO_IMAGE[self.value]
        WINDOW.blit(dice_image, pos)
