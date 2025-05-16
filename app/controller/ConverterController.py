from app.model.users import Users
from app.model.performances import Performances

from app import app, db
from app.model import response
from flask import request
from flask_jwt_extended import *
from datetime import datetime
import os
import time
import numpy as np
import soundfile as sf
from pydub import AudioSegment
import ffmpeg
import torch
from app.helper import PostProcessingHelper as post_helper
from app.helper import PreProcessingHelper as pre_helper
from app.helper import Predict
from mutagen.mp3 import MP3

@app.route('/api/convert/<initial>/<inputType>', methods=['POST'])
def convert(initial, inputType):
    try:
        initial_song = request.files["song"]

        timestamp = int(datetime.timestamp(datetime.now()))
        filename_initial = initial_song.filename[:-4]+"_"+str(timestamp)+".mp3"
        initial_full_path = os.path.join(app.config['UPLOAD_FOLDER'], filename_initial)
        initial_song.save(initial_full_path)

        print(os.path.exists(initial_full_path))
        while not os.path.exists(initial_full_path):
            time.sleep(1)

        if os.path.isfile(initial_full_path):
            print("mp3 to mel")
            file_awal = pre_helper.mp3_to_mel(initial_full_path)
            
            if ('mfcc' == inputType.lower()):
                print("mel to mfcc")
                file_awal = pre_helper.mel_to_mfcc(file_awal)
            print(file_awal.shape)

            if (initial=="Piano"):
                 jenis="p2g"
                 target="Guitar"
            elif (initial=="Guitar"):
                 jenis="g2p"
                 target="Piano"

            jenis += "_" + inputType.lower()

            prediction = Predict.predict(file_awal,jenis)

            # post-processing
            print("post-processing...")

            # convert to waveform
            print("converting back to waveform")
            hasil = post_helper.mel_to_wave(prediction)

            # save jadi wav
            print("saving wav...")
            filename_target_wav = initial_song.filename[:-4]+"_"+str(timestamp)+".wav"
            target_full_path = os.path.join(app.config['UPLOAD_FOLDER'], filename_target_wav)
            sf.write(target_full_path, hasil, 22050, subtype='PCM_24')

            while not os.path.exists(target_full_path):
                time.sleep(1)

            if os.path.isfile(target_full_path):
                # convert to mp3
                print("converting to mp3...")
                sound = AudioSegment.from_wav(target_full_path)
                timestamp = int(datetime.timestamp(datetime.now()))
                filename_target = initial_song.filename[:-4]+"_"+str(timestamp)+".mp3"
                hasil_full_path = os.path.join(app.config['UPLOAD_FOLDER'], filename_target)
                sound.export(hasil_full_path, format='mp3')

            # bersihkan file initial wav & mp3
            print("finishing...")
            os.remove(initial_full_path)
            os.remove(target_full_path)

            while not os.path.exists(hasil_full_path):
                time.sleep(1)

            audio = MP3(hasil_full_path)
            duration = audio.info.length

            performance = Performances(user=1, title=filename_target, initial=initial, target=target, duration=duration, gdrive_link='')
            db.session.add(performance)
            db.session.commit()

            # Move the file
            src = os.path.abspath(os.path.join(os.path.dirname(__file__), '../temp/')) + '\\' + filename_target
            dst = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../Staccata/public/Song')) + '\\' + filename_target
            os.rename(src, dst)
            print("done!")

        return response.success({
            "title": initial_song.filename[:-4],
            "id": performance.id,
            "file_path": filename_target,
            "duration": duration
        }, "success")
    except Exception as e:
        return response.serverError({}, e)