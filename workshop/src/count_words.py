#!/usr/bin/env python

import argparse

parser = argparse.ArgumentParser(description='Compare two English-language strings for semantic similarity.')

def wordCount(mystring):  
    tempcount = 0  
    count = 1  

    try:  
        for character in mystring:  
            if character == " ":  
                tempcount +=1  
                if tempcount ==1:  
                    count +=1  
                else:  
                    tempcount +=1
            else:
                 tempcount=0

        return count  

    except Exception:  
        error = "Not a string"  
        return error  

def sentence_diff():

    mystring = "I   am having   a    very nice 23!@$      day."           

    print(wordCount(mystring)) 

def compare():

    from difflib import SequenceMatcher
    a = "Dump Administration Dismisses Surgeon General Vivek Murthy (http)PUGheO7BuT5LUEtHDcgm"
    b = "Dump Administration Dismisses Surgeon General Vivek Murthy (http)avGqdhRVOO"
    ratio = SequenceMatcher(None, a, b).ratio()
    print(ratio)

def main():

    sentence_diff()

if __name__ == "__main__":
    main()
