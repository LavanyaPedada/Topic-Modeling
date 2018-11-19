# -*- coding: utf-8 -*-
"""
Created on 2018-08-10

@author: 290015835

Python 3.6
"""

########################## Final code###############
from lxml import etree
###Check all files are zip under zip then xml files format
import pandas as pd
import numpy as np
from os import listdir
import zipfile, re, io


in_path = 'C:\\Users\\290015835\\Documents\\VOC Satisfaction\\Call Transcripts\\Vail_CDR_Transcripts_Nov17/'
out_path = 'C:\\Users\\290015835\\Documents\\VOC Satisfaction\\Call Transcripts\\Nov_transcripts_csv/'


filenames = listdir(in_path)

for x in filenames:
    
    
    # define variables(i.e. tags) from file we care about
    # store text in dict for each file 
    var_dict = {
    
        'call_id': [],
        'eureka_id' : [],
        'wav_length_sec' : [],
        'total_silence_sec': [],
        'word_count' : [],
        'Customer' : [],
        'Agent' : []
        
    }

    # create empty DF to store 
    features = list(var_dict.keys())

    out_df = pd.DataFrame(columns = features)
    
    filename = in_path + x #zip name
    
    
    with zipfile.ZipFile(filename, 'r') as zfile:
                
        for name in zfile.namelist(): #xml name
            
            f = zfile.open(name)
            
            try: #to prevent non xml file error
                
                tree = etree.parse(f)
                root = tree.getroot()
                                
                speaker = root.xpath('//segment/speaker/text()')
                words = root.xpath('//segment/words/text()')
                times = root.xpath('//segment/start_time_relative/text()')
                                
                for feature in features:
                    
                    if (feature == 'Customer') or (feature == 'Agent'):
                        
                        tmp_index = [i for i, j in enumerate(speaker) if j == feature]
                                                
                        speaker_words = [words[w] for w in tmp_index]
                        speaker_times = [times[t] for t in tmp_index]
                        
                        var_dict[feature].append([speaker_words, speaker_times]) 
                        
                        
                    else:
                        tmp = root.find(feature).text
                        var_dict[feature].append(tmp)
            
            except:
                print('ive passed on file ' + name)
                pass
            
                
        for feature in features:
            out_df[feature] = var_dict[feature]
            
        
        out_file = out_path + 'call_miner_' + str(x) + '.csv'
        
        out_df.to_csv(out_file, index = False)
