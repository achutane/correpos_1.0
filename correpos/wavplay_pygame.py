# -*- coding: utf-8 -*-
"""
Created on Sun Sep 18 19:02:09 2016

@author: M Y
"""
import pygame.mixer

def play(wav, volume):
    
    wavfile="./wav_SE/"+wav+".wav"

    pygame.mixer.init()
    wav=pygame.mixer.Sound(wavfile)

    wav.set_volume(volume*0.01) #パラメータは0.0~1.0の浮動小数点です 
    wav.play() # loop count
