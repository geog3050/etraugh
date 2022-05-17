#Author: Ethan Traugh
#Last changed 2/1/22

#dictionary of folding temps
fold_temps = {
    "tropical" : 30,
    "continental": 25,
    "other" : 18
}

#Prints whether plant is folded or unfolded depending on climate and temperatures
def CheckData(climate, temps):
    #if input data is correct type
    if InputCheck(climate, temps) == True:
        
        #if given climate isn't in dictionary, use value for key "other"
        if climate.lower() in fold_temps:
            fu_temp = fold_temps[climate.lower()] 
        else:
            fu_temp = fold_temps["other"]
        
        #if temperature is lower than or equal to foldingtemp, print F. Otherwise, print U
        for temp in temps:
            if (temp <= fu_temp):
                print("F")
            else:
                print("U")


#if input is not proper type, return false, otherwise, return true
def InputCheck(s, l):
    if type(s) is not str:
        print("Climate not given as string")
        return False
    if type(l) is not list:
        print("Temperatures not given as list")
        return False
    for temp in l:
        if type(temp) is not float:
            print(str(temp) + " is not a float")
            return False
    return True

#takes user input, checks for correct types, prints F or U depending on given climate and folding temps
def TakeInput():
    print("Climate Type:")
    climate = input()
    print("Temperatures:")
    temps = eval(input())
    CheckData(climate, temps)

TakeInput()
