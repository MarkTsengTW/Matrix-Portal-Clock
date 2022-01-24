# Matrix Portal Generic Clock
# Sometimes it seems like electronics hobbyists are obsessed with clocks. Everyone wants to build one and put their own twist on it.
# I'm sharing this code to make things easier for Matrix Portal clock builders. You are welcome to adapt and build on it.
# The aim was to make a clock with simpler and more adaptable code than others out there, by making greater use of the MatrixPortal class.
# You will need to do some work to turn it into your own finished product.
# That might include changing the font and colour, or writing the code to display 12-hour time.
# Have fun!

# Set up Python
import time
import board
import terminalio
from adafruit_matrixportal.matrixportal import MatrixPortal

# Set up secrets
from secrets import secrets

# Set up the Matrix Portal
matrixportal = MatrixPortal(width = 64, height = 32, debug=False) # Set debug=True to show text area updating with the time.
network = matrixportal.network

# Get internet time and set the interval to check it again
network.get_local_time()
internet_time_check_interval = 86400 # Every 24 hours.
next_internet_time_check = time.monotonic() + internet_time_check_interval

# Time debugging
print("Internet time details:", time.localtime()) # If you look at the whole struct, you will see it contains more than just the time of day...
print("Next internet time check in", next_internet_time_check, "seconds.")

# Create a text object for the clock face on the matrix. We can add the time later.
# You can change the font, text position and other properties here. The colour is set in the update_time function.
matrixportal.add_text(
text_font=terminalio.FONT,
text_position=((matrixportal.graphics.display.width // 2) - 15, (matrixportal.graphics.display.height // 2))
)

# Send the current time to the clock face
def update_clock(internet_time):
    hours = internet_time.tm_hour # This results in 24 hour time. If you want to convert to 12 hour time this is where you do it.
    minutes = internet_time.tm_min
    matrixportal.set_text(str(hours) + ":" + str(minutes)) # IDs can be specified to work with multiple text objects.
    matrixportal.set_text_color(0x0000FF) # The clock is blue by default. The colour is set here so it can be changed while the clock is runnning.

# Main loop
while True:
    internal_time = time.monotonic()
    if internal_time > next_internet_time_check:
            network.get_local_time()
            print("Syncronised to internet time.")
            next_internet_time_check = (internal_time + internet_time_check_interval)
    update_clock(time.localtime())
    time.sleep(1) # This results in the main loop running once every second.
