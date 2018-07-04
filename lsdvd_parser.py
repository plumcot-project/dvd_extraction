from xml.dom import minidom
import subprocess
import os 

class Track:
    def __init__(self, ix, length):
        self.title = str(ix)
        self.duration = float(length)  
        
''' Process the lsdvd command and return the file '''

def lsdvd():
    with open(os.devnull, mode='w') as f:
        doc = subprocess.check_output(
        ['lsdvd', '-x', '-Ox', '/dev/dvd'] , stderr = f)
    return doc 
    
''' Encode and recode the file to make sure there is no encoding problem  '''
    
def recode(doc):
    doc = doc.decode('utf-8', 'ignore').replace('&', '')
    doc = doc.encode('utf-8')
    return doc
    
''' Return the title written in the file '''
    
def get_contentTitle(content):
    contentTitle = content.getElementsByTagName('title')[0].firstChild.data
    return contentTitle
    
''' Return the list of the tracks in the file with their title and duration '''
    
def get_tracks(content):
    track = content.getElementsByTagName('track')
    tracks = []

    i = 0

    for t in track:
        ix = t.getElementsByTagName('ix')[0]
        length = t.getElementsByTagName('length')[0]
        
        t = Track(ix.firstChild.data, length.firstChild.data)
        tracks.append(t)
    return tracks
    
''' Return the list of real episodes from the tracks list '''    

def get_episodes(tracks):
    episodes = []
    nbEpisodes = int(input('How many episodes ?'))

    if nbEpisodes > 1 and tracks[0].duration > tracks[1].duration*1.5 :
        firstTitleContainsAll = True
    else:
        firstTitleContainsAll = False

    if firstTitleContainsAll:
        for i in range(1,nbEpisodes+1):
            episodes.append(tracks[i])
    else:
        for i in range(0,nbEpisodes+0):
            episodes.append(tracks[i])
    return episodes     
    
''' Return the tracks list sorted by their duration (top-down) '''    
    
def sort_tracks(tracks):
    swap = True
    i = 0
    while swap == True:
        swap = False
        i = i + 1
        for j in range(0, len(tracks)-i):
            if tracks[j].duration < tracks[j+1].duration:
                swap = True
                tracks[j],tracks[j+1] = tracks[j+1],tracks[j]
    return tracks
    
'''
def get_duree(Piste):
    return Piste.duree
    
sorted(pistes, key=pistes.get_duree, reverse=True)
'''

''' Display the tracks '''
            
def print_tracks(tracks):
    for t in tracks:
        print('Title ' + t.title + ' : ' + str(t.duration))              

''' Display the episodes '''
        
def print_episodes(episodes):
    i = 1
    for e in episodes:
        print('Episode ' + str(i) + ' : title -> ' + e.title + ' | duration -> ' + str(e.duration))
        i += 1



''' ############################################### '''
'''                    MAIN                         '''
''' ############################################### '''


doc = lsdvd()
doc = recode(doc)

content = minidom.parseString(doc)
print('Content title : ' + get_contentTitle(content))

tracks = get_tracks(content)
tracks = sort_tracks(tracks)

print_tracks(tracks)

episodes = get_episodes(tracks)
        
print_episodes(episodes)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    