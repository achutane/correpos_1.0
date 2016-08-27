# -*- coding: utf-8 -*-
import wave
import pyaudio

#起動しないで，終了しない

# 音をだす
def play(wav, time):
    
    wf = wave.open(wav+".wav", "r")
    # ストリーム開始
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    data = wf.readframes(1024)
    t=0;
    while(t<time):
        stream.write(data)
        data = wf.readframes(1024)
        t=t+1
    stream.close()      # ストリーム終了
    p.terminate()


if __name__ == '__main__':
    play("test", 100)
    
    
    
    
    
