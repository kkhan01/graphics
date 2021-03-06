from display import *
from matrix import *
from math import *

def add_box( points, x, y, z, w, h, d ):
    
    #defining points -- vertices
    p0 = [x, y, z]
    p1 = [x, y, z - d]
    p2 = [x, y - h, z]
    p3 = [x, y - h, z - d]
    p4 = [x + w, y, z]
    p5 = [x + w, y, z - d]
    p6 = [x + w, y - h, z]
    p7 = [x + w, y - h, z - d]
    
    # add edges based off vertices
    add_edge(points, p0[0], p0[1], p0[2], p1[0], p1[1], p1[2])
    add_edge(points, p0[0], p0[1], p0[2], p2[0], p2[1], p2[2])
    add_edge(points, p0[0], p0[1], p0[2], p4[0], p4[1], p4[2])
    
    add_edge(points, p6[0], p6[1], p6[2], p4[0], p4[1], p4[2])
    add_edge(points, p6[0], p6[1], p6[2], p2[0], p2[1], p2[2])
    add_edge(points, p6[0], p6[1], p6[2], p7[0], p7[1], p7[2])

    add_edge(points, p3[0], p3[1], p3[2], p2[0], p2[1], p2[2])
    add_edge(points, p3[0], p3[1], p3[2], p7[0], p7[1], p7[2])
    add_edge(points, p3[0], p3[1], p3[2], p1[0], p1[1], p1[2])

    add_edge(points, p5[0], p5[1], p5[2], p7[0], p7[1], p7[2])
    add_edge(points, p5[0], p5[1], p5[2], p4[0], p4[1], p4[2])
    add_edge(points, p5[0], p5[1], p5[2], p1[0], p1[1], p1[2])
    
def add_sphere( points, cx, cy, cz, r, step ):
    temp = []
    generate_sphere( temp, cx, cy, cz, r, step )
    for i in temp:
        add_edge( points, i[0], i[1], i[2], i[0] + 1, i[1], i[2] )

def generate_sphere( points, cx, cy, cz, r, step ):
    i = 0
    while i <= step:
        factor = float(i)/step
        phi = 2 * math.pi * factor
        j = 0
        while j <= step:
            factor = float(j)/step
            theta = math.pi * factor
            x = r * math.cos(theta) + cx
            y = r * math.sin(theta) * math.cos(phi)+ cy
            z = r * math.sin(theta) * math.sin(phi)+ cz
            add_point(points, x, y, z)
            j += 1
        i += 1

def add_torus( points, cx, cy, cz, r0, r1, step ):
    temp = []
    generate_torus( temp, cx, cy, cz, r0, r1, step )
    for i in temp:
        #print i
        add_edge( points, i[0], i[1], i[2], i[0] + 1, i[1], i[2] )
def generate_torus( points, cx, cy, cz, r0, r1, step ):
    i = 0
    while i <= step:
        factor = float(i)/step
        phi = 2 * math.pi * factor
        j = 0
        while j <= step:
            factor = float(j)/step
            theta = 2 * math.pi * factor
            x = math.cos(phi) * (r0 * math.cos(theta) + r1) + cx
            y = r0 * math.sin(theta) + cy
            z = -math.sin(phi) * (r0 * math.cos(theta) + r1) + cz 
            add_point(points, x, y, z)
            j += 1
        i += 1

def add_circle( points, cx, cy, cz, r, step ):
    x0 = r + cx
    y0 = cy
    i = 1
    while i <= step:
        t = float(i)/step
        x1 = r * math.cos(2*math.pi * t) + cx;
        y1 = r * math.sin(2*math.pi * t) + cy;

        add_edge(points, x0, y0, cz, x1, y1, cz)
        x0 = x1
        y0 = y1
        i+= 1

def add_curve( points, x0, y0, x1, y1, x2, y2, x3, y3, step, curve_type ):

    xcoefs = generate_curve_coefs(x0, x1, x2, x3, curve_type)[0]
    ycoefs = generate_curve_coefs(y0, y1, y2, y3, curve_type)[0]

    i = 1
    while i <= step:
        t = float(i)/step
        x = xcoefs[0] * t*t*t + xcoefs[1] * t*t + xcoefs[2] * t + xcoefs[3]
        y = ycoefs[0] * t*t*t + ycoefs[1] * t*t + ycoefs[2] * t + ycoefs[3]

        add_edge(points, x0, y0, 0, x, y, 0)
        x0 = x
        y0 = y
        i+= 1

def draw_lines( matrix, screen, color ):
    if len(matrix) < 2:
        print 'Need at least 2 points to draw'
        return
    
    point = 0
    while point < len(matrix) - 1:
        draw_line( int(matrix[point][0]),
                   int(matrix[point][1]),
                   int(matrix[point+1][0]),
                   int(matrix[point+1][1]),
                   screen, color)    
        point+= 2
        
def add_edge( matrix, x0, y0, z0, x1, y1, z1 ):
    add_point(matrix, x0, y0, z0)
    add_point(matrix, x1, y1, z1)
    
def add_point( matrix, x, y, z=0 ):
    matrix.append( [x, y, z, 1] )
    



def draw_line( x0, y0, x1, y1, screen, color ):

    #swap points if going right -> left
    if x0 > x1:
        xt = x0
        yt = y0
        x0 = x1
        y0 = y1
        x1 = xt
        y1 = yt

    x = x0
    y = y0
    A = 2 * (y1 - y0)
    B = -2 * (x1 - x0)

    #octants 1 and 8
    if ( abs(x1-x0) >= abs(y1 - y0) ):

        #octant 1
        if A > 0:            
            d = A + B/2

            while x < x1:
                plot(screen, color, x, y)
                if d > 0:
                    y+= 1
                    d+= B
                x+= 1
                d+= A
            #end octant 1 while
            plot(screen, color, x1, y1)
        #end octant 1

        #octant 8
        else:
            d = A - B/2

            while x < x1:
                plot(screen, color, x, y)
                if d < 0:
                    y-= 1
                    d-= B
                x+= 1
                d+= A
            #end octant 8 while
            plot(screen, color, x1, y1)
        #end octant 8
    #end octants 1 and 8

    #octants 2 and 7
    else:
        #octant 2
        if A > 0:
            d = A/2 + B

            while y < y1:
                plot(screen, color, x, y)
                if d < 0:
                    x+= 1
                    d+= A
                y+= 1
                d+= B
            #end octant 2 while
            plot(screen, color, x1, y1)
        #end octant 2

        #octant 7
        else:
            d = A/2 - B;

            while y > y1:
                plot(screen, color, x, y)
                if d > 0:
                    x+= 1
                    d+= A
                y-= 1
                d-= B
            #end octant 7 while
            plot(screen, color, x1, y1)
        #end octant 7
    #end octants 2 and 7
#end draw_line
