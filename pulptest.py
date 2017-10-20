"""
線形計画法 pulp tutrial
"""
import requests
import io
from PIL import Image
from pulp import *


response = requests.get("https://pbs.twimg.com/media/DMDvNNSUQAIr8SH.jpg")
img_data = io.BytesIO(response.content)
img = Image.open(img_data)
img.show()




problem = LpProblem("Button Problem",LpMaximize)
Count_A = LpVariable("A Button",0,100,"Integer")
Count_B = LpVariable("B Button",0,100,"Integer")
Count_C = LpVariable("C Button",0,100,"Integer")

problem += (Count_A*10 + Count_B*0 + Count_C * -10) - (Count_A*20 + Count_B*-10 + Count_C * -20)
problem += Count_A + Count_B + Count_C <=100
problem += (Count_A*10 + Count_B*0 + Count_C * -10) >= 0
problem +=  (Count_A*20 + Count_B*-10 + Count_C * -20) >= 0

problem.writeLP("ButtonProb.lp")
problem.solve()
print("Status:", LpStatus[problem.status])

print (problem)

result=0
Me =(Count_A.value()*10 + Count_B.value()*0 + Count_C.value() * -10)
You=(Count_A.value()*20 + Count_B.value()*-10 + Count_C.value() * -20)

for v in problem.variables():
    print(v.name, "=", v.varValue)

result+= Count_A.value()* -10
result += Count_B.value() *10
result += Count_C.value() *10

print("\n\nResult")
print("差額 :{0}万円".format(result))

print("\n")
print("私の所持金 : {} 万円".format(Me))
print("あなたの所持金 : {} 万円".format(You))