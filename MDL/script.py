import mdl
from display import *
from matrix import *
from draw import *

def run(filename):
    """
    This function runs an mdl script
    """
    global view
    view = [0,
            0,
            1];
    global ambient
    ambient = [50,
               50,
               50]
    global light
    light = [[0.5,
              0.75,
              1],
             [0,
              255,
              255]]
    global areflect
    areflect = [0.1,
                0.1,
                0.1]
    global dreflect
    dreflect = [0.5,
                0.5,
                0.5]
    global sreflect
    sreflect = [0.5,
                0.5,
                0.5]

    global color
    color = [0, 0, 0]
    tmp = new_matrix()
    ident( tmp )

    global stack
    stack = [ [x[:] for x in tmp] ]
    global screen
    screen = new_screen()
    global zbuffer
    zbuffer = new_zbuffer()
    global temp
    tmp = []
    global step_3d
    step_3d = 20
    #extra variables, but they help me
    global polygons
    polygons = []
    global edges
    edges = []

    #executes the mdl commands
    def execute(line, args):
        #variables
        global view
        global ambient
        global light
        global areflect
        global dreflect
        global sreflect
        global color
        global stack
        global screen
        global zbuffer
        global tmp
        global step_3d
        #extra variables, but they help me
        global polygons
        global edges
        
        #loop!    
        if line == 'push':
            stack.append( [x[:] for x in stack[-1]] )
        elif line == 'pop':
            stack.pop()
        elif line == 'display' or line == 'save':
            if line == 'display':
                display(screen)
            else:
                save_extension(screen, str(args[0]) + str(args[1]))
        elif line == 'sphere':
            add_sphere(polygons,
                       float(args[0]), float(args[1]), float(args[2]),
                       float(args[3]), step_3d)
            matrix_mult( stack[-1], polygons )
            draw_polygons(polygons, screen, zbuffer, view, ambient, light, areflect, dreflect, sreflect)
            polygons = []
        elif line == 'torus':
            add_torus(polygons,
                      float(args[0]), float(args[1]), float(args[2]),
                      float(args[3]), float(args[4]), step_3d)
            matrix_mult( stack[-1], polygons )
            draw_polygons(polygons, screen, zbuffer, view, ambient, light, areflect, dreflect, sreflect)
            polygons = []
        elif line == 'box':
            add_box(polygons,
                    float(args[0]), float(args[1]), float(args[2]),
                    float(args[3]), float(args[4]), float(args[5]))
            matrix_mult( stack[-1], polygons )
            draw_polygons(polygons, screen, zbuffer, view, ambient, light, areflect, dreflect, sreflect)
            polygons = []
        elif line == 'line':
            add_edge( edges,
                      float(args[0]), float(args[1]), float(args[2]),
                      float(args[3]), float(args[4]), float(args[5]) )
            matrix_mult( stack[-1], edges )
            draw_lines(eges, screen, zbuffer, color)
            edges = []
        elif line == 'scale':
            t = make_scale(float(args[0]), float(args[1]), float(args[2]))
            matrix_mult( stack[-1], t )
            stack[-1] = [ x[:] for x in t]
        elif line == 'move':
            t = make_translate(float(args[0]), float(args[1]), float(args[2]))
            matrix_mult( stack[-1], t )
            stack[-1] = [ x[:] for x in t]
        elif line == 'rotate':
            theta = float(args[1]) * (math.pi / 180)
            if args[0] == 'x':
                t = make_rotX(theta)
            elif args[0] == 'y':
                t = make_rotY(theta)
            else:
                t = make_rotZ(theta)
            matrix_mult( stack[-1], t )
            stack[-1] = [ x[:] for x in t]
        return
        
            

    p = mdl.parseFile(filename)
    
    if p:
        #print p
        (commands, symbols) = p
        #print '###################'
        #print commands
        #print len(commands)
        #print len(commands[1])
        #print '###################'
        #print symbols
                
        for i in range(0, len(commands)):
            command = commands[i][0]
            args = []
            for j in range(1, len(commands[i])):
                args.append(commands[i][j])
            #print (command, args)
            execute(command, args)
    else:
        print "Parsing failed."
        return
