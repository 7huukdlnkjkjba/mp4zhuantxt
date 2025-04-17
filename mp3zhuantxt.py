from pydub import AudioSegment
import speech_recognition as sr
import os

media_path = r"D:\下载\wake.mp4"  # 支持mp3或mp4

# 自动生成wav和txt文件名
base, ext = os.path.splitext(media_path)
wav_path = base + ".wav"
txt_path = base + ".txt"

# 判断文件类型并读取音频
if ext.lower() == ".mp3":
    audio = AudioSegment.from_mp3(media_path)
elif ext.lower() == ".mp4":
    audio = AudioSegment.from_file(media_path, format="mp4")
else:
    raise ValueError("仅支持MP3或MP4文件")

audio = audio.set_channels(1).set_frame_rate(16000)
audio.export(wav_path, format="wav")

# 加载音频并识别每 60 秒一段
recognizer = sr.Recognizer()
with sr.AudioFile(wav_path) as source:
    total_duration = int(audio.duration_seconds)
    print("总时长：", total_duration, "秒")

    result_text = ""
    for i in range(0, total_duration, 60):
        print(f"识别第 {i} 秒到 {min(i+60, total_duration)} 秒...")
        source_audio = recognizer.record(source, duration=60)
        try:
            text = recognizer.recognize_google(source_audio, language='zh-CN')
            result_text += text + "\n"
        except Exception as e:
            result_text += f"[第 {i} 秒识别失败：{e}]\n"

# 写入文本
with open(txt_path, "w", encoding="utf-8") as f:
    f.write(result_text)

# 删除wav文件
if os.path.exists(wav_path):
    os.remove(wav_path)
    print(f"{wav_path} 已删除。")

print(f"识别完成！结果已保存到 {txt_path}")