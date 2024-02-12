import string
import random

class PassWordGenerate:
    # numberには生成したい文字数から3引いた数字を指定する
    def alphabet_big_small_number(self, number):
        # 文字セットを作成：数字、英大文字、英小文字
        digits = string.digits  # 数字
        uppercase = string.ascii_uppercase  # 英大文字
        lowercase = string.ascii_lowercase  # 英小文字

        # それぞれの文字を必ず1文字以上使用するために1文字ずつ選択
        random_digit = random.choice(digits)
        random_upper = random.choice(uppercase)
        random_lower = random.choice(lowercase)

        # 残りの8文字をランダムに選択
        remaining_chars = ''.join(random.choices(digits + uppercase + lowercase, k=number))
        result = random_digit + random_upper + random_lower + remaining_chars
        # 文字列を一文字ずつ分解し、それぞれ一つの要素としてリストに格納
        result_list = list(result)
        random.shuffle(result_list)
        code = ''.join(result_list)
        return code

password_generate = PassWordGenerate()