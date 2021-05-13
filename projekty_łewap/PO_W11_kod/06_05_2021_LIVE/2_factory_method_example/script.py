from shape import CircleCreator, SquareCreator

shape_creator = SquareCreator()
shape = shape_creator.create_shape()
area = shape.count_area()
print(f"Area: {area}")
