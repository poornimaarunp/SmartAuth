import os
from time import sleep
import glob
import numpy as np

from utils import feature
from utils import fileread
from utils import recordaudio
from utils import model


class SmartAuthInterface(object):
    
    def enrollinterface(self,dir):
        self.readRecording(dir)
        self.enrollModelling(dir)
    
    def authenticateinterface(self,user,dir):
        print ("Welcome...")
        self.authRecording(user,dir)
        validation_1=self.authenticateModelling(user,dir)
        validation = validation_1
        count=0
        while(not validation) & (count!=2):
            print ("\nI am finding it a bit hard today to hear you. Can you try once again?")
            print("\n")
            self.authRecording(user, dir)
            validation = self.authenticateModelling(user, dir)
            count=count+1
            if validation:
                break

        if validation:
            print("\nWelcome {} !! Have a good day!".format(user))
            print("\n")
        else:
            print ("\nSorry! We couldn't identify you. Have you registered?")
            print("\n")


    def authenticateModelling(self,user,dir):
        authfolder="{0}/{1}/".format(user,dir)
        user_features=feature.get_signal(user,dir)
        m = model.GMMmodel()
        validation = m.validate_model(user_features[0],user_features[1])
        return validation

    def enrollModelling(self,dir):
        user_features=feature.process_signal(dir)
        m = model.GMMmodel()
        m.generate_model(user_features[0],user_features[1])
    
    def readRecording(self,dir):
        if not os.path.exists(dir):
            os.makedirs(dir)
        os.chdir(dir)
        
        sleep(1)
        print ("You are about to start enrollment.....")
        sleep(1)
        print ("Read the below text to start...")
        sleep(1)
        recordaudio.record_multiple_times(1)
        print ("We want to identify you accurately... Lets try one more time..")
        # sleep(1)
        print ("Read the below text to start...")
        sleep(1)
        recordaudio.record_multiple_times(2)
        print ("Now, this is final and we are done !!")
        # sleep(1)
        print ("Read the below text to start...")
        sleep(1)
        recordaudio.record_multiple_times(3)

    def authRecording(self, user,dir):
        curdir = os.path.abspath(os.curdir)
        authfolder="{0}/{1}".format(user,dir)
        if not os.path.exists(authfolder):
            os.makedirs(authfolder)
        os.chdir(authfolder)

        print ("Read the below text to authenticate...")
        sleep(1)
        recordaudio.record_multiple_times(2)
        
        os.chdir(curdir)
        
    def convert_audio(self,path_to_file):
        sample_rate, samples = fileread.read_wav(path_to_file)
        freq,time,spect = fileread.get_spectrogram(sample_rate,samples)
        fileread.show_spectrogram(freq,time,spect)

    def initialize(self):
        DATASET = "bin/dataset"
        MODELS = "bin/models"
        m = model.GMMmodel()
        directories = glob.glob(os.path.abspath(os.curdir) + "/" + DATASET + "/*")
        data = []
        target = []
        if not os.path.isdir(os.path.abspath(os.curdir) + "/" + MODELS):
            os.mkdir(MODELS, mode=0o777)

        for dir in directories:
            dirsplit = dir.split('/')
            name = dirsplit[len(dirsplit) - 1].split('-')[0]
            name = dirsplit[len(dirsplit) - 1]
            print("Learning:",name)

            features = np.asarray(())
            wavs = glob.glob(dir + "/wav/*.wav")
            if len(wavs) > 0:
                for wav in wavs:
                    vector = feature.get_features(wav)
                    if features.size == 0:
                        features = vector
                    else:
                        features = np.vstack((features, vector))
                m.development_model(features,MODELS,name)