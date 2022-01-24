

# User Inputs 
#keyString = str(input("Enter the Secret Key: "))
#plainText = input("Enter the Message: ")

#ORIGINAL 
#plainText = '10111101' 
#keyString = '1010000010'

#PART B
plainText = '01010101' 
keyString = '1000100111'

#PART C
#plainText = '01010100'
#keyString = '0001110011'

# Create Tuples of permutation numbers
Permutate10 = (3,5,2,7,4,10,1,9,8,6)
Permutate8 = (6,3,7,4,8,5,10,9)
ExpansionPermutation = (4,1,2,3,2,3,4,1)
InitialPermutation = (2,6,3,1,4,8,5,7)
FinalPermutation = (4, 1, 3, 5, 7, 2, 8, 6) #Inverse of IP
p4 = (2,4,3,1)

# S-Box Creation
sboxes0 = [[1,0,3,2],[3,2,1,0],[0,2,1,3],[3,1,3,2]]
sboxes1 = [[0,1,2,3],[2,0,1,3],[3,0,1,0],[2,1,0,3]]
sboxesModified = [[3,1,3,2],[3,2,1,0],[0,2,1,3],[1,0,3,2]]

def permutate(keyString, permutation):
    permutatedString = [] #Creates a temporary list container 
    #Use each char from the provided permutation to be stored as the index of the keyString
    for index in permutation:
        index = int(index) #Convert index back into an interger      
        permutatedString.append(keyString[index-1]) #Append each int into the list
        permString = ''.join(map(str, permutatedString))#Join the elements of the list into one string
    return permString

# Takes in the secret key as a string, finds the middle, 
# and splits it into 2 4 bit keys
def keyReturn(keyString):   
    length = len(keyString) #finds the length of the input string (key)
    midLength = int(length/2) #gets the middle of the string
    global keyL 
    keyL = keyString[:midLength] #Returns the 0-middle of the string to the global variable keyL
    global keyR
    keyR = keyString[midLength:] #Returns the middle to the end of the global variable keyR
    return keyL, keyR

# Takes in a key and shifts the characters around by a specified number
def keyShift(key, numberofShifts):
    bitString = str(key) #Converts the key into a string for easy manipulation 
    #Starting at sub number of shifts to end, concatenate it with 0 to sub number of shifts to create the shifted key
    shiftedKey = str(bitString[numberofShifts:]) + str(bitString[:numberofShifts]) 
    return shiftedKey

# Rejoin the split keys into a permutated key
def stringCombine(shiftedKeyL, shiftedKeyR):
    combinedLRKey = shiftedKeyL + shiftedKeyR
    return combinedLRKey

def permEP(IP, sk1orsk2):
    keyReturn(IP) #Takes in an input and splits into keyL and keyR
    EpermR = permutate(keyR, ExpansionPermutation) #Takes the right side of the split and expands it to 8 bits
    #Perform xor on the expanded right side and sk1. The output is used in the s-boxes
    xored = int(EpermR, 2) ^ int(sk1orsk2, 2)
    xored = bin(xored); xored = str(xored); xored = xored[2:]
    keyReturn(xored)#Split the result of the xored permutation
    print("sk1orsk2:", sk1orsk2)

# Function to create input for the s-boxes, returns s0 and s1 as strings 
def sboxCreation(input0, input1):
    global s0
    s0 = []
    global s1
    s1 = []
    for s00 in input0:
        s00 = int(s00)
        s0.append(s00)
    for s01 in input1:
        s01 = str(s01)
        s1.append(s01)
    s0 = ''.join(map(str, s0))#Join the elements of the list into one string
    s1 = ''.join(map(str, s1))#Join the elements of the list into one string

    while len(s0) < 4:
        s0 = str(0) + s0 #pad leading 0 
    while len(s1) < 4:
        s1 = str(0) + s1 #pad leading 0 
    print("s0:", s0)
    print("s1:", s1)

#SBox Manipulations, takes in the output of sbox creation 
def sbox(s0, s1):
    #Row0
    a = (str(s0[0])); a = int(a)
    b = (str(s0[3])); b = int(b)
    sbox0Row = sboxesModified[a][b]
    ab = str(a) + str(b)
    ab = int(ab, 2)

    #Col0
    c = str(s0[1]);  c= int(c)
    d = str(s0[2]); d = int(d)
    sbox0Col = sboxesModified[c][d]
    cd = str(c) + str(d)
    cd = int(cd,2)

    sboxRow = sboxesModified[ab][cd]
    sboxRow = bin(sboxRow)
    sboxRow = str(sboxRow[2:])

    #Row1
    e = (str(s1[0])); e = int(e)
    f = (str(s1[3])); f = int(f)
    sbox1Row = sboxes1[e][f]
    ef = str(e) + str(f)
    ef = int(ef, 2)

    #Col1
    g = str(s1[1]); g = int(g)
    h = str(s1[2]); h = int(h)
    sbox1Col = sboxes1[g][h]
    gh = str(g) + str(h)
    gh = int(gh, 2)

    sboxRow1 = sboxes1[ef][gh]
    sboxRow1 = bin(sboxRow1)
    sboxRow1 = str(sboxRow1[2:])
    global sbox0
    sbox0 = stringCombine(sboxRow, sboxRow1)
    while len(sbox0) < 4:
        sbox0 = str(0) + sbox0 #pad leading 0 
    print("sbox", sbox0)

#SubKeys sk1 and sk2 are created using the P10, keyShift, and p8 functions
def keys(keyString, numberofShifts):
    global sk1 #initializes sk1
    p10 = permutate(keyString, Permutate10) #permutation 10
    keyReturn(p10) #split the 10 bit result into 2 5 bit strings
    ShiftkL = keyShift(keyL, numberofShifts) #Left shift one bit
    ShiftkR = keyShift(keyR, numberofShifts) #Left Shift one bit
    combStr = stringCombine(ShiftkL, ShiftkR) #Combine left and right shifted keys
    sk1 = permutate(combStr, Permutate8) #Perform p8 on newly combined string to create sk1
    print("sk1:", sk1)

    global sk2 #initializes sk2
    Shiftk2L = keyShift(ShiftkL, numberofShifts+1) #Left shift previously shifted L 2 bits
    Shiftk2R = keyShift(ShiftkR, numberofShifts+1) #Left Shift previously shifted R 2 bits
    combStr2 = stringCombine(Shiftk2L, Shiftk2R) # Combine these 2 sides 
    sk2 = permutate(combStr2, Permutate8) #Perform p8 permutation to create sk2
    print("sk2:", sk2)
    return sk1, sk2

def fk1(IPorSwap, sk1orsk2):
    permEP(IP, sk1orsk2) #This returns keyL, input into s0 and keyR, input into s1
    sboxCreation(keyL, keyR) #this returns s0 and s1 to be input into sbox function 
    sbox(s0, s1) #this takes in the output from sbox creation and returns a single 4 bit string sbox0
    print("If round 1, sk will be sk1. If round 2, sk will be sk2")
    print("sk1orsk2 :", sk1orsk2)
    perm4 = permutate(sbox0, p4)

    #xor keyL with perm4
    xoredp4 = int(keyL, 2) ^ int(perm4, 2)
    xoredp4 = bin(xoredp4); xoredp4 = str(xoredp4); xoredp4 = xoredp4[2:]
    while len(xoredp4) < 4:
        xoredp4 = str(0) + xoredp4 #pad leading 0 
    print("xoredp4:", xoredp4)
    keyReturn(xoredp4)#Split the result of the xoredp4 permutation
    keyReturn(IP)
    print("keyR:", keyR)
    global fk1Out
    fk1Out = stringCombine(xoredp4,keyR)
    keyReturn(fk1Out)#split into 2 parts
    global swap
    swap = stringCombine(keyR,keyL)#Swap

    print("fk1Out:", fk1Out)
    print("Swap:", swap)
    print('')
    print('')
    return swap

############# Function Section End, Program Section Begins Here #################

#Create the subkeys
keys(keyString, 1)
#Initial Permutation 
IP = permutate(plainText, InitialPermutation)
print("Initial Permutation:", IP)

#Perform the first fk function with subkey 1
print("")#spacing for easier output readability
print("-----------------------------------")
print("Function fk using subkey 1")
print("")
fk1(IP, sk1)
print("-----------------------------------")

#Perform the second round of fk using subkey 2
print("Second Round of fk function using subkey2")
print("")
fk1(swap, sk2)
print("------------------------------------")

#Final Cipher Text
cipher = permutate(swap, FinalPermutation)
print("Cipher Text:", cipher)
print('')

#This logic here is all wrong
print("------------------------------------")
print("Decryption")
print("")
fk1(cipher, swap)
fk1(fk1Out, keyString)