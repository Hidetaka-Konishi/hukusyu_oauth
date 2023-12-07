d = "M-1グランプリ, キングオブコント, R-1グランプリ"
da = ["お正月", "節分", "ひな祭り"]
db = ("ディズニーランド", "USJ", "ジブリパーク")
dc = {"肉体労働":"大工", "デスクワーク":"システムエンジニア"}

plus_join = ", ".join(d)
print(plus_join)

plus_join_2 = ", ".join(da)
print(plus_join_2)

plus_join_3 = ", ".join(db)
print(plus_join_3)

for i in dc.items():
    plus_join_4 = ":".join(i)
    print(plus_join_4)
