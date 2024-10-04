class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    
    
def Crypt(text, key):
    result = ""
    for i in range(len(text)):
        char = text[i]
        key_c = key[i % len(key)]
        result += chr((ord(char) + ord(key_c)) % 256)
    return result

def Decrypt(text, key):
    result = ""
    for i in range(len(text)):
        char = text[i]
        key_c = key[i % len(key)]
        result += chr((ord(char) - ord(key_c) + 256) % 256)
    return result
