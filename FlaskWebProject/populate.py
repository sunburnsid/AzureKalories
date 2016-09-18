from kalories import db
from kalories import Food, API
import csv

def initiate():
	db.create_all()

	pizza = Food('pizza', 12,36,10,7,11,6,2,0,False, 285, 'slice')
	db.session.add(pizza)
	burger = Food('burger', 20,29,17,12,0,38,0,3,False, 354, 'item')
	db.session.add(burger)
	coke = Food('cola', 0,39,0,0,0,0,12,0,False, 140, 'can')
	db.session.add(coke)
	red = Food('red bull', 1,2,3,4,5,6,7,9,True, 20, 'slice')
	db.session.add(red)
	donut = Food('donut', 1,2,3,4,5,6,7,9,True, 20, 'slice')
	db.session.add(donut)

	br = API(120316, "pizza", 2, '/static/yyy.png')
	lunch = API(130316, "burger", 1, '/static/yygg.png')
	din = API(120316, "cola", 3, '/static/yuy.png')

	db.session.add(lunch)
	db.session.add(br)
	db.session.add(din)

	db.session.commit()

def importCSV():
    db.create_all()
    with open('ABBREV.csv', 'rb') as csvfile:
        reader=csv.reader(csvfile)
        #x=0
        reader.next() #skip header
        for row in reader:
            #if (x<5):
                #print (row[1]+" "+ row[4]+" "+ row[7]+ row[5]+ row[10]+row[33]+row[31]+row[20]+row[43]+row[3]+row[49])
                #x+=1
            #Format: name, protein, carbs, fat, calcium, vitA, vitB, vitC, vitK, healthy, calories, unit
            #temp=Food(row[1], float(row[4]), float(row[7]), float(row[5]), float(row[10]),float(row[33]),float(row[31]),float(row[20]),float(row[43]),True,float(row[3]),row[49])
            temp=Food(row[1], row[4], row[7], row[5], row[10],row[33],row[31],row[20],row[43],True,row[3],row[49])
            db.session.add(temp)
            db.session.commit()

if __name__ == '__main__':
	initiate()
        #importCSV()
