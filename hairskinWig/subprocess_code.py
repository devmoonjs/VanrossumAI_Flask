import subprocess
import os
import tensorflow as tf

print(os.getcwd())
def prepro_image(command):
    subprocess.run(["python", command])

    result = "전처리 완료"
    return result

def synthesis_image(hair_synthesis_script, im_path1, im_path2, im_path3, sign, smooth):
    subprocess.run(["python", hair_synthesis_script, "--im_path1", im_path1, "--im_path2", im_path2, "--im_path3", im_path3, "--sign", sign, "--smooth", smooth])

    result = "합성 완료"
    return result
