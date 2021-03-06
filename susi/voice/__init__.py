""" Main Module of the SUSI Linux App
"""
import os
from ..config import SusiConfig
from .susi_loop import SusiLoop
from .player import player

cfg = SusiConfig()

def startup_sound():
    base_folder = cfg.get('path.base')
    audio_file = os.path.join(base_folder, 'data/wav/ting-ting_susi_has_started.wav')
    player.say(audio_file)


