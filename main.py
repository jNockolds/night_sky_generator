import turtle
import random
import colorsys

screen_width, screen_height = 1280, 720

screen = turtle.Screen()
screen.title("Starry Sky")
screen.setup(width=screen_width, height=screen_height)
screen.colormode(255)
screen.tracer(0)

pen = turtle.Turtle()
pen.hideturtle()
pen.pencolor("White")
pen.fillcolor("White")

def draw_circle(radius, fill=False):
    """Centred on turtle's position."""
    pen.teleport(pen.xcor(), pen.ycor() - radius)
    if fill == False:
        pen.circle(100)
    else:
        pen.begin_fill()
        pen.circle(radius)
        pen.end_fill()
    pen.teleport(pen.xcor(), pen.ycor() + radius)

def random_star_radius(r_min=0.5, r_max=3, exponent=-1.5) -> int:
    """
    Generate a star radius based on a power law distribution.
    
    Parameters:
    - exponent: the higher exponent is, the more large stars there are
    """
    number = random.random()
    
    radius = ( number * (r_max**exponent - r_min**exponent) + r_min**exponent )**(1/exponent)
    
    return radius

def get_apparent_brightness(colour):
    """Returns a value in range [0, 1] (including both end points) which represents the apparent brightness of the given.
    \nUses the formula 'brightness = ((0.299 * r) + (0.587 * g) + (0.114 * b)) / 255' because those coefficients of r, g, and b represent approximately how much human eyes weight the brightness of each colour (at least according to this paper: https://library.imaging.org/admin/apis/public/api/ist/website/downloadArticle/tdpf/1/1/art00005).
    """
    r = colour[0]
    g = colour[1]
    b = colour[2]

    return ((0.299 * r) + (0.587 * g) + (0.114 * b)) / 255 # brightness is weighted by how sensitive human eyes are to red, green, and blue on average

def adjust_apparent_brightness(colour, brightness):
    """Returns an adjusted version of the input colour with the given apparent brightness."""
    if brightness < 0 or brightness > 1:
        raise ValueError("brightness must be >= 0 and <= 1")

    base_brightness = get_apparent_brightness(colour)

    if base_brightness == 0:
        # grey with equivalent brightness:
        r = 255 * brightness
        g = 255 * brightness
        b = 255 * brightness
    
    else:
        r = colour[0]
        g = colour[1]
        b = colour[2]

        scale_factor = brightness / base_brightness

        r *= scale_factor
        if r > 255:
            r = 255

        g *= scale_factor
        if g > 255:
            g = 255

        b *= scale_factor
        if b > 255:
            b = 255

    return (int(r), int(g), int(b))

def get_saturation(colour):
    colour = tuple(x/255 for x in colour) # normalising
    colour = colorsys.rgb_to_hsv(colour[0], colour[1], colour[2])
    return colour[1]

def adjust_saturation(colour, saturation):
    colour = tuple(x/255 for x in colour) # normalising
    colour = colorsys.rgb_to_hsv(colour[0], colour[1], colour[2])
    colour = colorsys.hsv_to_rgb(colour[0], saturation, colour[2])
    colour = tuple(x*255 for x in colour) # converting back to [0,255]
    return (int(colour[0]), int(colour[1]), int(colour[2]))

def random_sky_colour(print_colour=True):
    r = int(round(8 * random.random()))
    g = int(round(8 * random.random()))
    b = int(round(20 * random.random()))
    
    while b < r or b < g or r < g: # keeps it primarily grey, blue, and red
        r = int(round(8 * random.random()))
        g = int(round(8 * random.random()))
        b = int(round(20 * random.random()))
    
    if print_colour:
        print(f"night sky colour: {(r, g, b)}")

    return (r, g, b)

def shift_num_in_range(number, input_range : list, output_range : list, is_int=False):
    """
    E.g. shift_num_in_range(0.5, 0, 1, 0.5, 1) returns 0.75
    Parameters:
    - input_range: the range (inclusive) of the input values
    - output_range: the range (inclusive) of the output values
    """
    len_in = input_range[1] - input_range[0]
    len_out = output_range[1] - output_range[0]

    # finding position in input range:
    number -= input_range[0]
    position = number / len_in

    if is_int:
        return int(round((len_out * position) + output_range[0]))
    return (len_out * position) + output_range[0]

def draw_stars(star_density=0.001, radius_min=0.5, radius_max=3):
    """
    Parameters:
    - star_density: the number of stars per pixel (typically ~ 0.001)
    """
    surface_area = screen_width * screen_height
    star_num = int(round(star_density * surface_area))

    star_coords = []
    for i in range(star_num):
        xcor = random.randint(-screen_width // 2, screen_width // 2)
        ycor = random.randint(-screen_height // 2, screen_height // 2)
        star_coords.append((xcor, ycor))

    for star in star_coords:
        radius = random_star_radius(radius_min, radius_max)

        colour = screen.bgcolor()
        colour = (int(colour[0]), int(colour[1]), int(colour[2])) # screen.bgcolor() returns float rgb values

        # altering brightness to make smaller stars less noticeable
        screen_brightness = get_apparent_brightness(colour)
        brightness = shift_num_in_range(radius, [radius_min, radius_max], [screen_brightness, 1], is_int=False) # screen_brightness is min_out to prevent stars appearing darker than the sky
        colour = adjust_apparent_brightness(colour, brightness)

        # altering saturation to keep stars looking mostly white
        saturation_multiplier = 0.2
        colour = adjust_saturation(colour, get_saturation(colour) * saturation_multiplier)

        pen.color(colour)
        pen.fillcolor(colour)

        pen.teleport(star[0], star[1])
        draw_circle(radius, True)

screen.bgcolor(random_sky_colour())

draw_stars()

turtle.update() # renders the drawings
turtle.done() # keeps screen open after drawing is complete
