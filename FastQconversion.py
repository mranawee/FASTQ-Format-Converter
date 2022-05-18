#!/usr/bin/env python3

# Group Members: Mano Ranaweera(mranawee) and Andrew Gjelsteen(agjelste)
"""
FastQconverter.py overview: FastQ files are taken in and parsed.
Different FastQ formats are converted from one to another.
input: FastQprint.py with initial FastQ file format
output: Wanted FastQ file format
"""
import math
import sys
class FastQreader :
    '''
    For reading in FastQ files
    '''
    def __init__ (self, fname=''):
        '''contructor: saves attribute fname '''
        self.fname = fname
        self.fastQchunk = [[],[],[],[]]
    def doOpen (self):
        ''' Handle file opens, allowing STDIN.'''
        if self.fname is '':
            return sys.stdin
        else:
            return open(self.fname)

    def readFastQ (self):
        """
        Read an entire FastQ record and yields a linecallable chunk of FastQfile
        """
        header = ''
        chunk = []

        with self.doOpen() as fileH:
            header = ''
            chunk = []
            
            # skip to first fasta header
            line = fileH.readline()
            while not line.startswith('@') :
                line = fileH.readline()
            header = line[:].rstrip()
            count = 0
            for line in fileH:
                if line.startswith ('@') and count == 3:
                    sequence = chunk[0]
                    optional = chunk[1]
                    quality = chunk [2]
                    
                    yield header, sequence, optional, quality
                    header = line[1:].rstrip()
                    chunk = []
                    count = 0
                else :
                    chunk.append(line.rstrip())
                    count +=1
        sequence = chunk[0]
        optional = chunk[1]
        quality = chunk [2]
        yield header, sequence, optional, quality
class FastQconverter:
    """
    Converts format of fastQfile through use of dictionary of conversion equations that utilize ASCII table access commands chr() and ord()
    input: quality line of fastQfile chunk
    output: new quality line in different format
    """
    formatConverter = {'P64':{'P33':lambda Q: chr(ord(Q)-31), 'P64': lambda Q: Q},
            'P33':{'P64': lambda Q: chr(ord(Q)+31), 'P33': lambda Q: Q},
            'P64B':{'P64': lambda Q: chr(ord(Q)), 'P33': lambda Q: chr(ord(Q)-31)},
            'P64SOL':{'P64': lambda Q: chr(int(-10*math.log(1/(1+10**((ord(Q)-64)/10)),10)+64)), 'P33':lambda Q: chr(int(-10*math.log(1/(1+10**((ord(Q)-64)/10)),10)+33))}}

    def __init__ (self):
        '''Initialize empty strings of chunks of FastQfile'''
        self.sequence = ''
        self.sequence = self.cleanSeq(self.sequence)
        self.quality = ''
        self.inFormat = ''
        self.outFormat = ''

    def cleanSeq (self,sequence):
        '''Clean sequence of unwanted symbols and replace with "N"'''
        nodotSeq = sequence.replace('.','N')
        nostarSeq = nodotSeq.replace('*','N')
        cleanedSeq = nostarSeq.replace('n','N')
        return (cleanedSeq)

    def convertFormat (self):
        '''Iterates through each letter of quality line and adds new converted value to empty string'''
        inString = ''
        count = 0
        for letter in self.quality:
            # print("each letter is: " + letter)
            if letter is ('B') and self.inFormat == 'P64B' : #adjusts for P64B feature where (Q<2 or ('@', 'A')) = 'B'
                inString += '@'
                # print("inString in if block: " + inString)
            else:
                inString += FastQconverter.formatConverter[self.inFormat][self.outFormat](letter)
                # print("this is inString: " + inString )
        return inString
