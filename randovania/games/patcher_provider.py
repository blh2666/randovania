from randovania.games.game import RandovaniaGame
from randovania.games.patcher import Patcher


class PatcherProvider:
    def __init__(self):
        from randovania.games.patchers import claris_patcher
        from randovania.games.patchers import randomprime_patcher
        from randovania.games.patchers import super_duper_metroid_patcher
        self._patchers = {
            RandovaniaGame.METROID_PRIME: randomprime_patcher.RandomprimePatcher(),
            RandovaniaGame.METROID_PRIME_ECHOES: claris_patcher.ClarisPatcher(),
            RandovaniaGame.SUPER_METROID: super_duper_metroid_patcher.SuperDuperMetroidPatcher(),
        }

    def patcher_for_game(self, game: RandovaniaGame) -> Patcher:
        return self._patchers[game]
