# Kyle Mayer
# 12/17/2014/I
# MADVLSI Final Project
# Olin Fall 2014
# Inductor Generator
# this code generates a .txt file (which can be renamed to a .mag file) that is interpretable by MAGIC.
# based on a few input variables (like size), it generates a massive spiral that can be used to attempt
# inductors on integrated circuits (not normally done because of the amount of space required).

Inductor_file = open('Inductor.txt','w', 0) # create the inductor file

file_text = "magic\ntech scmos\n" # creating header
file_text = file_text + "<< metal3 >>\n"

inductor_bounding_box = 3800 # number of lambda for the entire box
metal_thickness = 5 # design rules
metal_spacing = 3
locationX = 0 # where does the next loop start? should initialize to 0,0 and work its way towards the
# center as the loop runs
locationY = 0 # should always be the same as locationX. Optionally different incase you want to
# make a non square inductor. note that I don't have support for this yet.

lower_X = 0 # I know, I know, this is python. I don't need to declare variables.
lower_Y = 0 # habbits die hard, I guess.
upper_X = 0
upper_Y = 0

first_time = True # the first loop of the inductor has to be a little different
test_counter = 0 # used for debugging. allows you to create a partial inductor (stop before the spiral hits the center)

while inductor_bounding_box > 20: # leave a little bit at the end to do by hand, since I'm not sure
    # how this program will natively handle the boundry case.
    
    # case: vertical rectangle, left side. if this isn't the first time through the loop, then this needs to extend slightly
    # below
    if first_time == True:
        lower_Y = locationY
    else:
        lower_Y = locationY - metal_thickness - metal_spacing
    upper_X = lower_X + metal_thickness
    lower_X = locationX
    upper_Y = locationY + inductor_bounding_box # based on locationY, NOT lower_Y. This is because lower_Y can actually
    # be down below locationY to attach to the last loop.
    file_text = file_text + "rect " + str(lower_X) + " " + str(lower_Y) + " " + str(upper_X) + " " + str(upper_Y) + "\n"
    
    # case: horizontal rectangle, top. lower X should stay the same
    lower_Y = locationY + inductor_bounding_box - metal_thickness
    upper_Y = lower_Y + metal_thickness
    upper_X = lower_X + inductor_bounding_box
    file_text = file_text + "rect " + str(lower_X) + " " + str(lower_Y) + " " + str(upper_X) + " " + str(upper_Y) + "\n"
    
    # case: vertical rectangle, right. upper point should stay the same
    lower_X = upper_X - metal_thickness
    lower_Y = locationY
    file_text = file_text + "rect " + str(lower_X) + " " + str(lower_Y) + " " + str(upper_X) + " " + str(upper_Y) + "\n"
    
    # case: horizontal rectangle, bottom. lower Y and upper X should stay the same. also, this one doesn't close the loop!
    lower_X = locationX + metal_thickness + metal_spacing
    upper_Y = lower_Y + metal_thickness
    file_text = file_text + "rect " + str(lower_X) + " " + str(lower_Y) + " " + str(upper_X) + " " + str(upper_Y) + "\n"
        
    # for testing purposes, terminate this loop now.
    #inductor_bounding_box = 0
    
    # for testing purposes, terminate the loop after a few iterations rather than the entire inductor
    """
    if test_counter > 6:
        inductor_bounding_box = 0
    test_counter += 1
    """
    
    first_time = False
    
    # now, update the location and bounding box for the next loop
    locationX += metal_thickness + metal_spacing
    locationY += metal_thickness + metal_spacing
    inductor_bounding_box -= 2*(metal_thickness + metal_spacing) # the 2* is because we laid a trace on both sides of the box
    
    
file_text = file_text + "<< end >>"
Inductor_file.write(file_text)