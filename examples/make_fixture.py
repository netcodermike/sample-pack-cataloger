import wave,struct,math
with wave.open('examples/demo.wav','wb')as w:
 w.setparams((2,2,16000,0,'NONE','not compressed'))
 w.writeframes(b''.join(struct.pack('<hh',int(14000*math.sin(2*math.pi*220*i/16000)),int(7000*math.sin(2*math.pi*330*i/16000)))for i in range(16000)))
print('Created one-second synthetic stereo PCM16 recording')
