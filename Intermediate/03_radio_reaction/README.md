# RADIO REACTION GAME



## 1. About the game

The game uses the micro:bit radio to see which player can react the quickest.

One person is the referee.  Their micro:bit controls the game. The other people are players.  Their micro:bits listen out for a radio message from the referee to start the game.

When they receive the message, the players’ micro:bits change the image on the display.  When they see this, all the players try to press their Button A as quickly as possible.

As soon as Button A is pressed, the player’s micro:bit sends out a radio message with the player’s name.

The referee’s micro:bit listens out for these messages.  The winner is the first message received.  The winner’s name is shown on the referee’s display and sent out as a radio message to the player’s micro:bits, which also show the winner’s name.

Then the referee can start a new game.

![picture of runners](media/image1.png)


---
**We want one person to program their micro:bit as the referee that controls the game. Everyone else programs their micro:bits to play the game. Decide which you are going to be, then jump to section 2 or section 3.**

---



## 2. Referee

Open the editor and create a new program. Type a comment to explain what the program does, then add the import statements to include the micro:bit and radio functions we need.

```python
# Radio reaction time game - referee

from microbit import display, Image, button_a
import radio
```

The referee sends out two types of messages: a “go” message to start each game, and a “winner” message with the name of the player who reacts first. Add these lines to your program to define what these messages will be.  Also add a constant to control how fast messages scroll on the display; the smaller the number the faster the scroll.

```python
GO_MESSAGE = "go"
WINNER_PREFIX = "winner: "
SCROLL_SPEED = 50
```

[TBC]

```python
OUR_GROUP = 73 # ask your mentor what group number to use
```

Now add code to configure the radio to only broadcast to our group of micro:bits and then turn the radio on.  Then add code to display a message and icon.  The icon tells the referee that they can press Button A when they want to start the game.

```python
radio.on()
radio.config(group=OUR_GROUP)

display.scroll("referee ready", SCROLL_SPEED)
display.show(Image.TARGET)
```

Now add a while loop that will loop forever.  Each time round the loop is one round of the game.

```python
while True:
```

At the start of each game, the program must wait for the referee to press Button A.  Add this while loop to keep checking if the button has been pressed.  The code inside the loop receives and throws away any old radio messages that happen to be received, so that they don’t interfere with the game.

```python
    while not button_a.was_pressed():
        message = radio.receive()
```

When Button A is pressed, the program broadcasts the “go” message and changes the display, so the referee knows that the game is working.  Add this code.  Be careful to indent it correctly.

```python
    radio.send(GO_MESSAGE)
    display.show(Image.CONFUSED)
```

Now the program needs to listen out for any received radio messages.  Add this code.

```python
    message = radio.receive()
    while message is None:
        message = radio.receive()
```

This while loop ends and the program continues as soon as the first message is received. 

This message will contain the player’s name, so add this code to broadcast the winner to all the players and scroll it on the display.  The last line of code changes the display back to the icon, so the referee knows they can start another round when they want to.

```python
    radio.send(WINNER_PREFIX + message)
    display.scroll(WINNER_PREFIX + message, SCROLL_SPEED)
    display.show(Image.TARGET)
```

> Download the program to the micro:bit now to make sure there are no errors.


---
**Find someone with the player program so you can test your referee program.**

---



## 3. Player



@@@@@@@@@@@@@@

Open the Mu editor and create a new program.  Type a comment to explain what the program does, then add the import statements to include the micro:bit and radio functions we need.

```python
# Radio beacon for micro:bit

from microbit import display, Image, sleep
import radio
```

The beacon will send out a message every few seconds.  You need to say what the message is and how often it is sent, so add these lines to your program.

```python
MESSAGE = "dojo"
INTERVAL = 5
```

You can choose your own message, but keep it short.  The `INTERVAL` is the number of seconds between sending messages.  Don’t make it too quick – 5 is a good number.

[TBC]

```python
OUR_GROUP = 42 # ask your mentor what group number to use
```

Because you can’t see radio messages, add a statement to show something on the micro:bit display, just so you know that the program is running.

```python
display.show(Image.YES)
```

> Download the program to the micro:bit now; you should see a tick mark on the display.

Next, add the code to broadcast the message.  Start by configuring the radio to only broadcast to our group of micro:bits and then turn the radio on.

```python
radio.config(group=OUR_GROUP)
radio.on()
```

Now add a loop that sends the message and sleeps before repeating.

```python
while True:
    radio.send(MESSAGE)
    sleep(INTERVAL * 1000)
```

> Download the program to the micro:bit again and make sure you can still see the tick mark on the display.

---
**Find someone with the receiver program so you can test the beacon.**

---



## 3. Receiver

Open the Mu editor and create a new program.  Type a comment to explain what the program does, then add the import statements to include the micro:bit and radio functions we need.

```python
# Radio receiver for micro:bit

from microbit import display, Image, sleep
import radio
```

[TBC]

```python
OUR_GROUP = 42 # ask your mentor what group number to use
```

So that you know the program is running, add a statement to show something on the micro:bit display.

```python
display.show(Image.SQUARE_SMALL)
```

> Download the program to the micro:bit now; you should see a square on the display.

Now add the code to receive and display messages. Start by configuring the radio to only receive from our group of micro:bits and then turn the radio on.

```python
radio.config(group=OUR_GROUP)
radio.on()
```

Now add a loop that checks if a message has been received and scrolls it if it has.

```python
while True:
    message = radio.receive()
    if message:
        display.scroll(message, delay=50)
        display.show(Image.SQUARE_SMALL)
```


> Download the program to the micro:bit again and make sure you can still see the square on the display.

---
**Find someone with the beacon program so you can test the receiver.**

---



