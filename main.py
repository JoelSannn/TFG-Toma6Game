# Author: Joel Sánchez de Murga Pacheco
# TFG: Desenvolupament d’una aplicació del joc de cartes ¡Toma 6! incloent agents intel·ligents com a jugadors
# Year: 2023-24

from controller.controller import *
from PyGame.PyGame import *
import tensorflow as tf
import os
import logging

if __name__ == "__main__":
    pygame = PygameGame()
    pygame.menu()