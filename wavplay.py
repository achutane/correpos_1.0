# -*- coding: utf-8 -*-
import wave
import pyaudio

# 音をだす
def play(wav, mTime):
    
    wavfile="./wav_SE/"+wav+".wav"
    wf = wave.open(wavfile, "r")
    # ストリーム開始
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    data = wf.readframes(1024)
    t=0;
    while(t<mTime):
        stream.write(data)
        data = wf.readframes(1024)
        t=t+1
    stream.close()      # ストリーム終了
    p.terminate()


if __name__ == '__main__':
    #play(ファイル名, 時間ms)
    play("bird05", 100)
    play("chime08", 100)
    play("chime14", 100)
    play("dog01", 100)
    play("system46", 100)
    play("tiger01", 100)
    
    
    
    
    
    
    
