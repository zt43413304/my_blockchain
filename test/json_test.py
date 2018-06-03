import json

answer1 = {
    "1":'A', "2":'D',"3":'D',"4":'C',"5":'A',"6":'D',"7":'B',"8":'A',"9":'A',"10":'D'
}

ans = json.dumps(answer1)
# print(ans)
# print(ans[1], ans[2])

answer = '{"1": "A", "2": "D", "3": "D", "4": "C", "5": "A", "6": "D", "7": "B", "8": "A", "9": "A", "10": "D"}'
answer2 = '{1: "A", 2: "D", 3: "D", 4: "C", 5: "A", 6: "D", 7: "B", 8: "A", 9: "A", 10: "D"}'
ans = json.loads(answer)
print(ans, type(ans))
print(ans['1'])