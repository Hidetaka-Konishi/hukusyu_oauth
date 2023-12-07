d = {"賞レース":"M-1グランプリ, キングオブコント, R-1グランプリ", "賞レース２":"女芸人ナンバーワン決定戦, 歌ネタ王, NHK新人漫才決定戦"}
da = {"上半期":["お正月", "節分", "ひな祭り"], "下半期":["七夕", "ハロウィン", "クリスマス"]}

d_items = d.items()
da_items = da.items()

print(d_items)
print(da_items)

for day_one, schedule_one in d_items:
    schedule_one_plus = ", ".join(schedule_one)

    print(schedule_one_plus)

for day_one_2, schedule_one_2 in da_items:
    schedule_one_plus_2 = ", ".join(schedule_one_2)

    print(schedule_one_plus_2)
