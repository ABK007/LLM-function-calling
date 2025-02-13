def calculate_area_square(side:int ) -> int:
    """calculate area of square based on given parameters

    Args:
      side: length of one side of square.

    Returns: Area of the square.
    """
    
    print("Calculating the area of square")
    area = side * side
    
    print(f"Area of the square: {area}")
    

def calculate_area_rectangle(length:int, width:int ) -> int:
    """calculate area of rectangle based on given parameters

    Args:
      length: length of rectangle.
      width: width of rectanle

    Returns: Area of the rectangle.
    """
    
    print("Calculating the area of rectangle")
    area = length * width
    
    print(f"Area of the rectangle: {area}")


def calculate_area_triangle(base:int, height:int ):
    """calculate area of triangle based on given parameters

    Args:
      base: length of base of triangle.
      height: height of triangle.

    Returns: Area of the triangle.
    """
    
    print("Calculating the area of triangle")
    area = (base * height) / 2
    
    print(f"Area of the triangle: {area}")
    
   