#!/usr/bin/env python

import time
import scrollphathd


def scroll_message(message):
    # Clear the display and reset scrolling to (0, 0)
    scrollphathd.clear()
    length = scrollphathd.write_string(message)  # Write out your message
    scrollphathd.show()                          # Show the result
    # Initial delay before scrolling
    time.sleep(0.5)

    length -= scrollphathd.width

    # Now for the scrolling loop...
    while length > 0:
        # Scroll the buffer one place to the left
        scrollphathd.scroll(1)
        scrollphathd.show()                      # Show the result
        length -= 1
        # Delay for each scrolling step
        time.sleep(0.02)

    # Delay at the end of scrolling
    time.sleep(0.5)


scroll_message("Test")
