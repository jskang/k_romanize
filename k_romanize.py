#!/usr/bin/python
# Author:   JinSung Kang
# Email:    gogs14@hotmail.com
# Comments: The program transliterates korean into english, gets a file that is
#           a UTF-8 and returns a UTF-8 file with the transliteration

import codecs
import sys
# Starting positions for the cosonants in unicode hex
jaeumStart = [0xAC00, 0xAE4C, 0xB098, 0xB2E4, 0xB530, 0xB77C,
              0xB9C8, 0xBC14, 0xBE60, 0xC0AC, 0xC2F8, 0xC544,
              0xC790, 0xC9DC, 0xCC28, 0xCE74, 0xD0C0, 0xD30C,
              0xD558, 0xD7A4]
moeum = ['a', 'ae', 'ya', 'yae', 'eo', 'e', 'yeo', 'ye',
         'o', 'wa', 'wae', 'oe', 'yo', 'u', 'wo', 'we',
         'wi', 'yu', 'eu', 'ui', 'i']
jaeumInitial = ['g', 'kk', 'n', 'd', 'tt', 'r', 'm', 'b', 'pp',
                's', 'ss', '', 'j', 'jj', 'ch', 'k', 't', 'p', 'h']
badchim= ['', 'k', 'k', 'ks', 'n', 'nj', 'nt', 't', 'l', 'lk', 'lm', 'lp', 'ls',
          'lt', 'lp', 'lt', 'm', 'p', 'ps', 't', 't', 'ng', 't', 'k', 't', 't',
          'p', 't']
giuk = ['kg', '', 'ngn', 'kd', '', 'ngn', 'ngm', 'kb', '', 'ks', '', 'g', 'kj', '', 'kch', 'k-k', 'kt', 'kp', 'kh']
nieun = ['n-g', '', 'nn', 'td', '', 'nn', 'nm', 'nb', '', 'ns', '', 'n', 'nj', '', 'nch', 'nk', 'nt', 'np', 'nh']
digeut = ['tg', '', 'nn', 'td', '', 'nn', 'nm', 'tb', '', 'ts', '', 'd', 'tj', '', 'tch', 'tk', 't-t', 'tp', 't']
lieul = ['lg', '', 'll', 'ld', '', 'll', 'lm', 'lb', '', 'ls', '', 'r', 'lj', '', 'lch', 'lk', 'lt', 'lp', 'lh']
mieum = ['mg', '', 'mn', 'md', '', 'mn', 'mm', 'mb', '', 'ms', '', 'm', 'mj', '', 'mch', 'mk', 'mt', 'mp', 'mh']
bieup = ['pg', '', 'mn', 'pd', '', 'mn', 'mm', 'pb', '', 'ps', '', 'b', 'pj', '', 'pch', 'pk', 'pt', 'p-p', 'ph']
eeung = ['ngg', '', 'ngn', 'ngd', '', 'ngn', 'ngm', 'ngb', '', 'ngs', '', 'ng-', 'ngj', '', 'ngch', 'ngk', 'ngt', 'ngp', 'ngh']

badchimModified = [giuk, nieun, digeut, lieul, mieum, bieup, eeung]
maxJaeumPos = len(jaeumStart) - 1
transliterated = []

# testfile
f = codecs.open("testfile2.kor", 'r', 'utf-8')
# it uses to hold the data of each korean alphabet so that it can be processed
# more easily
class alphabet:
  def __init__(self, character):
    self.character = character
    self.charPos = ord(self.character)
    if self.charPos < jaeumStart[0] or self.charPos >= jaeumStart[maxJaeumPos]:
      self.isPunctuation = True
    else:
      self.isPunctuation = False

    if self.isPunctuation is False:
      self.unicodePos = int((self.charPos - jaeumStart[0]) / 588)
      self.jaPos = self.charPos - jaeumStart[self.unicodePos]
      self.moeumPos = int(self.jaPos / 28)
      self.badchimPos = self.jaPos % 28
      self.romanization = [jaeumInitial[self.unicodePos], moeum[self.moeumPos], '']

  def string(self):
    if self.isPunctuation is False:
      return self.romanization[0] + self.romanization[1] + self.romanization[2]
    else:
      return self.character

  def conversion(self, position, nextChar):
    if nextChar.unicodePos != 1 and \
       nextChar.unicodePos != 4 and \
       nextChar.unicodePos != 8 and \
       nextChar.unicodePos != 10 and \
       nextChar.unicodePos != 13 and \
       nextChar.unicodePos != 18:
      self.romanization[2] = badchimModified[position][nextChar.unicodePos]
    else:
      self.romanization[2] = badchim[character.badchimPos]
# Replace possible character that would screw up the process
lyrics = f.read().replace('\r\n', '\n').replace('\r', '\n')
lines = lyrics.split('\n')

# Go through the line
for arg in sys.argv:
  for line in lines:
    words = line.split(' ')
    for word in words:
      characters = list(word)
      characterList = []
      # Skips everything that is not korean and make a list of the number of
      # characters to process it later
      for character in characters:
        characterList.append(alphabet(character))
  
      wordLength = len(characterList)
      for i in range(wordLength):
        character = characterList[i]
        if character.isPunctuation is False and i < wordLength - 1:
	  if characterList[i + 1].isPunctuation is False:
	    if character.badchimPos == 2:
	      position = 0
	      character.conversion(position, characterList[i + 1])
	    elif character.badchimPos == 4:
	      position = 1
	      character.conversion(position, characterList[i + 1])
	    elif character.badchimPos == 7:
	      position = 2
	      character.conversion(position, characterList[i + 1])
	    elif character.badchimPos == 8:
	      position = 3
	      character.conversion(position, characterList[i + 1])
	    elif character.badchimPos == 16:
	      position = 4
	      character.conversion(position, characterList[i + 1])
	    elif character.badchimPos == 17:
	      position = 5
	      character.conversion(position, characterList[i + 1])
	    elif character.badchimPos == 21:
	      position = 6
	      character.conversion(position, characterList[i + 1])
	    else:
	      character.romanization[2] = badchim[character.badchimPos]
	  else:
	    character.romanization[2] = badchim[character.badchimPos]
        elif i >= wordLength - 1 and character.isPunctuation is False:
	  character.romanization[2] = badchim[character.badchimPos]
  
        transliterated.append(character.string())
      # Find out how to get badchim to collect
      # process the stuff in the alphabet
      transliterated.append(' ')
    transliterated.append('\n')
  print ''.join(transliterated)
