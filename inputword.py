import re

class WordCheck:
    def validate_password(self, password):
        if re.search(r'[^\x00-\x7F]', password) or len(password) < 14 or not re.search("[A-Z]", password) or not re.search("[a-z]", password) or not re.search("[0-9]", password):
            return False, "パスワードにはローマ字の大文字、小文字、数字を必ず一つ以上含めるようにして14文字以上であること。全角文字は使用できない。"
        return True, ""
    
    def big_word(self, word, message):
        if re.search(r'[^\x00-\x7F]', word):
            return False, f"{message}に全角文字は使用できません"
        return True, ""

word_check = WordCheck()