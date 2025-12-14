#a={"city":"madina","temp_c": 30 ,"is_weekend":"yah"}
#print(a.values())

row= [{"age":35, "city":""},
      {"age":"", "city":"madina"}
]

missing={"age":0, "city":0}
for i in row:
    for key in i:
        if i[key]=="":
            missing[key]= 1 


            
print(row)
print(missing)
