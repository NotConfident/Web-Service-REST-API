from PIL import Image, ImageDraw
from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask import Response
import json

class BoundingBox(): 
    def bb(): # Change it to include coordinates later down
        im = Image.new('RGB', (500, 300), (255, 255, 255)) # Size and color
        draw = ImageDraw.Draw(im)
        draw.rectangle((100, 50, 300, 200), fill=(0, 0, 0)) # x1, y1, x2, y2
        return im

class Animals():
    def __init__(self, age, color, weight): # init - called immediately when compiled
        self.age = age                      # self - to access current instance
        self.color = color  
        self.weight = weight

    def write(self):                        # incase it is needed
        return "Age:" , self.age, " Color:", self.color, " Weight:", self.weight

class Dog(Animals):
    def __init__(self, age, color, weight): 
        self.age = age
        self.color = color
        self.weight = weight
        self.type = "Dog"

    def write(self):
        return "Age:" , self.age, " Color:", self.color, " Weight:", self.weight, " Type:", self.type

class Cat(Animals):
    def __init__(self, age, color, weight):
        self.age = age
        self.color = color
        self.weight = weight
        self.type = "Cat"

    def write(self):
        return "Age:" , self.age, " Color:", self.color, " Weight:", self.weight, " Type:", self.type

class Horse(Animals):
    def __init__(self, age, color, weight):
        self.age = age
        self.color = color
        self.weight = weight
        self.type = "Horse"
    
    def write(self):
        return "Age:" , self.age, " Color:", self.color, " Weight:", self.weight, " Type:", self.type


class storage:
    def __init__(self, id, box, animals):
        self.id = id
        self.box = box
        self.animal = animals
    
    def write(self):
        return "Box Details:" , self.box, " Animal:", self.animal.type

objects = []
count = 0
js = []

class readID(Resource):
    def get(self):
        # global count
        # count = 0
        # print('{0:<8}{1:<8}{2:<12}{3:<8}{4:<8}'.format('ID', 'Age', 'Color', 'Weight', 'Type'))
        # for i in objects:
        #     # print('{0:<8}{1:<8}{2:<12}{3:<8}{4:<8}'.format(i.id, i.animal.age, i.animal.color, i.animal.weight, i.animal.type))
        #     # js.append([{ 'ID': i.ID,
        #     #         'Age': i.Age,
        #     #         'Color': i.Color,
        #     #         'Weight': i.Weight,
        #     #         'Type' : i.Type}])
        #     print(i['ID'])
        #     count+=1
        # print(data)

        return Response(json.dumps(objects),  mimetype='application/json')

class create(Resource):
    def post(self):
        parser = reqparse.RequestParser()  # initialize

        parser.add_argument('age', required=True)  # add arguments
        parser.add_argument('color', required=True)
        parser.add_argument('weight', required=True)
        parser.add_argument('animal_Type', required=True)

        args = parser.parse_args()  # parse arguments to dictionary
        global count 
        obj = globals()[args['animal_Type']]
        boxString = BoundingBox.bb()
        animalString = obj(args['age'], args['color'], args['weight'])
        boxAnimalString = storage(count, boxString, animalString)

        count+=1

        objects.append({ 'ID': count,
                    'Age': args['age'],
                    'Color': args['color'],
                    'Weight': args['weight'],
                    'Type' : args['animal_Type']})
        print(objects)
        return Response(json.dumps(objects[count - 1]),  mimetype='application/json')

# def create_old(age, color, weight, animal_Type):
#         global count
#         boxString = BoundingBox.bb()
#         animalString = animal_Type(age, color, weight)
#         boxAnimalString = storage(count, boxString, animalString)
#         objects.append(boxAnimalString)
#         count+=1

class update(Resource):
    def post(self):
        parser = reqparse.RequestParser()  # initialize

        parser.add_argument('id', required=True)  # add arguments
        parser.add_argument('age', required=True)
        parser.add_argument('color', required=True)
        parser.add_argument('weight', required=True)
        parser.add_argument('animal_Type', required=True)

        args = parser.parse_args()  # parse arguments to dictionary
        global count 
        index = int(args['id']) - 1 # ID starts from 1, but List starts from 0
        obj = globals()[args['animal_Type']]
        boxString = BoundingBox.bb()
        animalString = obj(args['age'], args['color'], args['weight'])
        boxAnimalString = storage(count, boxString, animalString)
    
        objects[index] = ({ 'ID': count,   # Updating
                    'Age': args['age'],
                    'Color': args['color'],
                    'Weight': args['weight'],
                    'Type' : args['animal_Type']})
        print(objects)

        return Response(json.dumps(objects[index]),  mimetype='application/json')

# def update_old(id,  age, color, weight, animal_Type):
#     objects[id].animal.age = age
#     objects[id].animal.color = color
#     objects[id].animal.weight = weight
#     objects[id].animal.type = animal_Type.__name__ # Shows the name of class instead of <class '__main__.ClassName'>

class readIndex(Resource):
    def get(self):
        data = json.dumps(objects)
        parser = reqparse.RequestParser()  # initialize

        parser.add_argument('id', required=True)  # add arguments

        args = parser.parse_args()  # parse arguments to dictionary

        index = int(args['id']) - 1 # ID starts from 1, but List starts from 0

        return Response(json.dumps(objects[index]),  mimetype='application/json')

# def read_Indexed_ID_old(id):
#     display(objects[id].box)
#     return objects[id].animal.type
    
class deleteByID(Resource):
    def get(self):
        data = json.dumps(objects)
        parser = reqparse.RequestParser()  # initialize

        parser.add_argument('id', required=True)  # add arguments

        args = parser.parse_args()  # parse arguments to dictionary

        index = int(args['id']) - 1 # ID starts from 1, but List starts from 0

        objects.pop(index)
        return Response(json.dumps(objects),  mimetype='application/json')

def deleteByID_old(id):
    objects.remove(objects[id])
    


# create_old(10, 'Red', 12, Dog)
# create_old(8, 'Maroon', 20, Cat)
# create_old(3, 'Purple', 15, Horse)
# create_old(9, 'Neon Blue', 18, Cat)
# create_old(4, 'Crimson', 10, Dog)
# create_old(9, 'Amber', 14, Horse)


# readID.get(objects)
# update(1, 4, 'Yellow', 4, Horse)
# deleteByID(1)
# print("")
# readID.get(objects)

app = Flask(__name__)
api = Api(app)

api.add_resource(readID, '/readIDs')
api.add_resource(create, '/create')
api.add_resource(update, '/update')
api.add_resource(readIndex, '/readIndex')
api.add_resource(deleteByID, '/deleteByID')

if __name__ == '__main__':
    app.run(debug=False)


