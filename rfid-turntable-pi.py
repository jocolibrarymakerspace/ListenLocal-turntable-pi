#!/usr/bin/env python
# -*- coding: utf8 -*-

#This is the Raspberry Pi RFID turntable developed for the Johnson County Library.
#Complete tutorial at [COMING SOON]
#Original Arduino project at https://github.com/jocolibrarymakerspace/ListenLocal-turntable-arduino

#Links
#Johnson County Library - http://jocolibrary.org/
#Johnson County Library MakerSpace - https://www.jocolibrary.org/we-recommend/listen-local
#Listen Local - https://www.jocolibrary.org/we-recommend/listen-local

#It requires:
#- SPI-Py installed from https://github.com/lthiey/SPI-Py
#- MFRC522-python from https://github.com/mxgxw/MFRC522-python
#- VLC-python bindings from https://github.com/oaubert/python-vlc

#This code is based off of:
#- the Read.py example included with MFRC522-python
#- the VLC Python binding examples at http://git.videolan.org/?p=vlc/bindings/python.git;a=tree;f=generated;b=HEAD

#MFRC522 RFID reader wiring
#| Name | Pin # | Pin name   |
#|------|-------|------------|
#| SDA  | 24    | GPIO8      |
#| SCK  | 23    | GPIO11     |
#| MOSI | 19    | GPIO10     |
#| MISO | 21    | GPIO9      |
#| IRQ  | None  | None       |
#| GND  | Any   | Any Ground |
#| RST  | 22    | GPIO25     |
#| 3.3V | 1     | 3V3        |

#Next up:
#-Reliable volume control

#---Code begins below this line!---

#We import the GPIO library
import RPi.GPIO as GPIO

#We import the time library
import time

#We import the MFRC522 RFID reader library
import MFRC522

#We import the signal library
import signal

#We import the VLC python bindings library
import vlc

#We define the program state
continue_reading = True

# We capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    print "Ctrl+C captured, ending read."
    continue_reading = False
    GPIO.cleanup()  #We clean up the GPIO data
    player.stop()   #We stop VLC

# We hook the SIGINT data
signal.signal(signal.SIGINT, end_read)

# We create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

#We create objects of the VLC class
player = vlc.MediaPlayer()

#We define the VLC playlist
#Add as many tracks as you need, just make sure to respect the formatting!
playlist = ['/home/pi/01.mp3', '/home/pi/02.mp3', '/home/pi/03.mp3', '/home/pi/04.mp3']

#Create variables to store and compare uids
uid = ()
justread = ()

# Welcome message
print "Welcome to the Listen Local RFID turntable"
print "Press Ctrl-C to stop."

# This loop keeps checking for chips. If one is near it will get the UID and au$
while continue_reading:

    # Scan for cards
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    # If a card is found
    if status == MIFAREReader.MI_OK:
        print("Card detected")

        # We get the UID of the card
        (status,uid) = MIFAREReader.MFRC522_Anticoll()

        # If we have the UID, we continue
        if status == MIFAREReader.MI_OK:

            # We print the card UID
            #Alternatively you can display the card UID with
            #print ("Card UID: " str(uid[0]) + str(uid[1] + str(uid[2] + str(uid[3])
            print ("Card UID: " +str(uid[0:4]))

            #We compare the card's 'UID to whatever we might have just read
            if justread != uid:
                #This is where the music playing begins!
                if (uid[0]) == XXX and (uid[1]) == XXX: #Change the uid values to match your RFID tags
                player.stop()   #We stop playing any other track that might be playing
                print("I'm playing track XX!")  #We announce which track is about to be played
                player = vlc.MediaPlayer(playlist[0])   #We request the  track in the playlist list
                player.play() #We start playing the track we just loaded

                #Sample additional track playing block follows - uncomment and modify accordingly.
                #Add as many blocks as you have tracks to play.
                #elif (uid[0]) == XXX and (uid[1]) == XXX:
                #    player.stop()   #We stop playing any other track that might be playing
                #    print("I'm playing track XX!")  #We announce which track is about to be played
                #    player = vlc.MediaPlayer(playlist[X])   #We summon the corresponding track in the playlist list
                #    player.play() #We start playing the track we just loaded
                #elif (uid[0]) == XXX and (uid[1]) == XXX: #Change the uid values to match your RFID tags
                #player.stop()   #We stop playing any other track that might be playing
                #print("I'm playing track XX!")  #We announce which track is about to be played
                #player = vlc.MediaPlayer(playlist[0])   #We request the  track in the playlist list
                #player.play() #We start playing the track we just loaded

            #We store the card's uid into the justread variable for comparing later
            justread = uid #We change the value of justread to match the latest tag we read

            else:
                print("You're already playing that track!") #We let the user know that the track is being played (And we don't try playing it from the top)
                time.sleep(5) #If the same card is still on the reader, we take a 5 seconds break before polling for RFID again

#And we do it all over again!
