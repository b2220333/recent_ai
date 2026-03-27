#!/usr/bin/env python3
# encoding: utf-8

import numpy as np
import wave
import struct

# 1. 設定參數
sample_rate = 44100  # 取樣率 (每秒 44100 個點，CD 標準)
duration = 2.0       # 長度 (秒)
frequency = 440.0    # 頻率 (Hz, A4)
amplitude = 16000    # 音量 (16位元音訊最大值為 32767)

# 2. 生成時間軸與正弦波 (向量化運算)
t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
audio_data = amplitude * np.sin(2 * np.pi * frequency * t)

# 3. 轉為 16-bit 整數格式 (黑客搬運數據)
audio_data = audio_data.astype(np.int16)

# 4. 寫入 WAV 檔案
with wave.open("tone_440hz.wav", "w") as f:
    f.setnchannels(1)      # 單聲道
    f.setsampwidth(2)      # 2 bytes (16-bit)
    f.setframerate(sample_rate)
    # 將陣列轉為二進位流寫入
    for sample in audio_data:
        f.writeframes(struct.pack('h', sample))

print("音訊檔案已生成：tone_440hz.wav")