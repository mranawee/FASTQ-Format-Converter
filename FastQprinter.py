#!/usr/bin/env python3

# Group Members: Mano Ranaweera(mranawee) and Andrew Gjelsteen(agjelste)

import FastQconvert as FC
import math
class CommandLine() :
    '''
    
    The command line implements a standard command line argument parser with various argument
    options, a standard usage and help.
    attributes:
    all arguments received from the commandline using .add_argument will be
    avalable within the .args attribute of object instantiated from CommandLine.
    '''

    def __init__(self, inOpts=None) :
        '''
        Implement a parser to interpret the command line argv string using argparse.
        '''
        import argparse
        self.parser = argparse.ArgumentParser(description = 'Program prolog - a brief description of what this thing does',
            epilog = 'Program epilog - some other stuff you feel compelled to say',
            add_help = True,
            prefix_chars = '-',
            usage = '%(prog)s [options] -option 1[default] <input >output')
        self.parser.add_argument('-input', '--inFormat', type=str, nargs='?')  #selection of input format
        self.parser.add_argument('-output', '--outFormat', type=str, nargs='?') #selection of output format
        if inOpts is None :
            self.args = self.parser.parse_args()
        else :
            self.args = self.parser.parse_args(inOpts)
        
def main(inCL=None):
        '''
        Input formats:(P33, P64, P64B, P64SOL)
        Output formats: (P33, P64)
        
        '''
        if inCL is None:
            myCommandLine = CommandLine()
        else:
            myCommandLine = CommandLine(inCL)
        myReader = FC.FastQreader()
        myConverter = FC.FastQconverter()
        myConverter.inFormat = myCommandLine.args.inFormat
        myConverter.outFormat = myCommandLine.args.outFormat
        #count = 0
        for header, sequence, optional, quality in myReader.readFastQ():
            if len(quality) == len(sequence):
                print ('@'+header)
                print (sequence)
                print (optional)
                myConverter.quality = quality
                print (myConverter.convertFormat())
                #count += 1
                #print (count)
if __name__ == "__main__":
    main()
