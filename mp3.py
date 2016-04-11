import os
import random
import sys
from subprocess import call
"""
This script generate, concatanated MP3 files from a given folder with MP3 files.
The size of concatanated MP3 file can be given as paramter in <max_wrap_mp> parameter. 
Random shuffle of input MP3 files done before concatanating them. 

NOTE : You need to have MP3WRAP installed before executing this in your 
environment.

Paramters to be override before executing.
  orig_path = folder with original MP3 files
  generate_folder = folder to store newly concatanated MP3 files (Make sure this folder outside of original MP3 folder.) 
  max_wrap_mb = size of each concatanated MP3 file in MB

Author: Lasantha Ranaweera
Date : 10/04/2016
"""
def get_file_list(folder_path, file_list):
    sub_path_list = os.listdir(folder_path)
    for sub_path in sub_path_list:
        sub_full_path = os.path.join(folder_path, sub_path)
        if os.path.isfile(sub_full_path):
            file_list.append(sub_full_path)
        elif os.path.isdir(sub_full_path):
            get_file_list(sub_full_path, file_list)
        else:
            print "Unknown problem "+sub_full_path
            return
    return file_list

if __name__ == "__main__":
    try:
        orig_path = sys.argv[1] # set origianl mp3 folder path
        generate_folder = sys.argv[2] # set output mp3 folder path
        max_wrap_mb = sys.argv[3] # set size of wrapped mp3 file in MB
    except IndexError:
        print "Invlid CLI argument"
        sys.exit(0)


    if not os.path.isdir(orig_path):
        print "Original MP3 location is not valid folder"
        sys.exit(0)

    if not os.path.isdir(generate_folder):
        print "Generate MP3 location is not valid folder"
        sys.exit(0)

    if max_wrap_mb == None:
        max_wrap_mb = 200
    else:
        max_wrap_mb = int(max_wrap_mb)

    file_counter = 1
        
    file_list = []
    sub_dir_list = os.listdir(orig_path)

    ## build song file list

    for sub_dir in sub_dir_list:
        folder_counter = 0
        sub_path = os.path.join(orig_path, sub_dir)
        if os.path.isdir(sub_path):
            song_list = get_file_list(sub_path, [])
            for song_file in song_list:
                if song_file.endswith('.mp3') or song_file.endswith('.MP3'):
                    file_list.append(song_file)
                    file_counter = file_counter + 1
                    folder_counter = folder_counter + 1

        print sub_dir +" -> "+str(len(song_list))
        print sub_dir +" -> "+str(folder_counter)


    print "Total number of files "+str(file_counter)

    ## wrapping MP3 files
    gen_file_number = 1
    counter = 0
    for attempt in range(2, file_counter+1):
        rand_value = random.randint(0, file_counter-2)
        print "Random "+str(rand_value)
        
        generate_file = os.path.join(generate_folder, str(gen_file_number)+"_MP3WRAP.mp3")

        if not os.path.isfile(generate_file):
            call(["mp3wrap", "-v", generate_file, file_list[rand_value]])
        else:
            call(["mp3wrap", "-a", generate_file, file_list[rand_value]])
            gen_file_mb = os.path.getsize(generate_file)/(1024 * 1024)
            print generate_file+" -> "+str(gen_file_mb)
            if gen_file_mb > max_wrap_mb:
                gen_file_number = gen_file_number + 1
        
        del file_list[rand_value]
        counter = counter+1
        file_counter = file_counter-1
        
    #print file_list
    #call(["mp3wrap", "-a", generate_file, file_list[0]]) # append last file too.
    
