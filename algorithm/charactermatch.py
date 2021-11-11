import copy
import difflib


def character_match_abbr(word_std, abbr, word):
    if word.find(word_std) != -1:
        return True
    while word.find(abbr[0]) != -1 and word.find(abbr[0]) + 3 <= len(word):
        word = word[word.find(abbr[0]):]
        copy_abbr = copy.deepcopy(abbr)
        flag = True
        for i in range(3):
            index = copy_abbr.find(word[0])
            if index == -1:
                flag = False
                break
            else:
                copy_abbr = copy_abbr[index:]
                word = word[1:]
        if flag:
            return True
        else:
            continue
    return False


def character_match(word_std, word):
    word, word_std = word.lower().replace("_", ""), word_std.lower()
    if word.find(word_std) != -1 or difflib.SequenceMatcher((lambda x: x in ["_", "/"]), word, word_std).ratio() > 0.9:
        return True
    else:
        return False


def word_match(word_std_list, word):
    for word_std in word_std_list:
        if character_match(word_std, word):
            return True
        else:
            continue
    return False


if __name__ == '__main__':
    print(word_match(["password", "pwd", "psw", "pswd"], "pwd"))
    print(word_match(["password", "pwd", "psw", "pswd"], "psw"))
    print(word_match(["password", "pwd", "psw", "pswd"], "psd"))
    print(word_match(["password", "pwd", "psw", "pswd"], "userpwd"))
    print(word_match(["password", "pwd", "psw", "pswd"], "user_psw_1"))
    print(word_match(["password", "pwd", "psw", "pswd"], "pwa"))
    print(word_match(["password", "pwd", "psw", "pswd"], "passw"))
    print(word_match(["password", "pwd", "psw", "pswd"], "passpsw"))
    print(word_match(["password", "pwd", "psw", "pswd"], "user_password_a"))
    print(word_match(["password", "pwd", "psw", "pswd"], "psw_a"))
