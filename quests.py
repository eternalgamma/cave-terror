import npc, player, items

class Quests:
    def __init__(self):
        raise NotImplementedError("Do not create raw Quest objects.")

    def __str__(self):
        return self.name