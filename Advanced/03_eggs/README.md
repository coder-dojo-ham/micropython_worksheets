# IT'S RAINING EGGS



## 1. About the game

With eggs raining down from the sky, it is your job to move a basket to catch as many as you can. Each egg will appear in a random position on the top row of LEDs, so use the buttons to move the basket left and
right across the bottom row. Each time the eggs move down, a new egg will appear on the top row.



![](.//media/image1.png)



The game has three parts:

-   starting (displaying the basket, starting a game timer)

-   playing the game (adding eggs, displaying them, moving them down the display, moving the basket)

-   finishing (displaying a message to say how many eggs you caught)

The program is written using Python’s **object oriented programming** features. Each part of the program (the basket, the eggs and the overall game) is written as an object that bundles up all the code and data it
needs to work.

In this game, it means we can write the code for an egg just once and not have to duplicate it for each egg that drops. Using objects also makes it easier to change or add to programs.

---
**You have already used objects when programming the micro:bit. The code for `display` is written as an object, with methods such as `display.scroll()` and `display.set_pixel()`.**

---




## 2. Create the game object

Open the Mu editor and click `New` to create a new program file. Write a comment to say what the program does. Then add the `import` statements to access the micro:bit features we need. We will be using random numbers in the program, so import that Python module too.

Then add the code for the game object using the Python keyword `class`. The class is called `EggGame`. It has methods to start, play the game and finish. For now, these just print debugging messages. The `__init__()` method is called automatically when an instance of EggGame is created. So as soon as this happens in the main program at `game = EggGame()`, the game will run.

---
**Be careful how you type `__init__()`. It has two underline characters before and two underline characters after the “init”. In Python, this is called “dunder” for double underline.**

---


```python
# Egg catching game for micro:bit

from microbit import display, button_a, button_b, running_time
import random

class EggGame:
	def __init__(self):
		self.start()
		self.play()
		self.finish()

    def start(self):
        display.scroll("start")
        def play(self):
        display.scroll("play")

    def finish(self):
        display.scroll("finish")

# Main program
if __name__ == "__main__":
	# execute only if run as a script
	game = EggGame()
```

Remember to save the file every few minutes as you work through the project.

Flash the program to the micro:bit. It should display the three debug messages in turn. If you see Python errors scrolling across the LEDs, check your code carefully.



## 3. Add useful constants

To make the code easier to understand and change, add these constant value definitions.

> Add this code near the top of the program after the `import` statements.


```python
# Timing constants
GAME_LENGTH = 20 # seconds
TICK = 1000 # milliseconds

# Display coordinate constants
MIN_X = 0
MAX_X = 4
MIN_Y = 0
MAX_Y = 4
BASKET_START_X = 2
BASKET_Y = 4
EGG_START_Y = 0

# Display LED constants
BASKET_BRIGHTNESS = 9
EGG_BRIGHTNESS = 3
OFF_BRIGHTNESS = 0
```



## 4. Add the basket

Now add the code for the `Basket` class. For now, it has just three methods. 

When we create the instance of `Basket`, the `__init__()` method will automatically set the basket’s x coordinate to the value `BASKET_START_X`.

The methods `show()` and `hide()` will be used by our game code to display the basket in the right position, as controlled by the buttons.

> Add this code after the constant definitions and before the `EggGame` class. 

```python
class Basket:

	def __init__(self):
		self.x = BASKET_START_X
	
	def show(self):
		display.set_pixel(self.x, BASKET_Y, BASKET_BRIGHTNESS)
	
	def hide(self):
		display.set_pixel(self.x, BASKET_Y, OFF_BRIGHTNESS)
```

If you flash the micro:bit now, you will not see the basket. We need to create an instance of the object *and* write the code to move it.

Change the `EggGame` so it looks like the code below. Be careful to make sure it matches exactly.

Work through the logic inside the `move_basket()` method to make sure you understand what’s happening.

The changes to the `play()` method also add the game timer to the program.

​```python
class EggGame:

	def __init__(self):
		self.basket = Basket()
		self.start_time = 0
		self.start()
		self.play()
		self.finish()

	def move_basket(self):
		current_x = self.basket.x
		if button_a.was_pressed():
			# move left
			if current_x > MIN_X:
				self.basket.hide()
				self.basket.x = current_x - 1
		elif button_b.was_pressed():
			# move right	
			if current_x < MAX_X:
				self.basket.hide()
				self.basket.x = current_x + 1
		self.basket.show()

	def start(self):
		self.start_time = running_time()
		self.basket.show()

	def play(self):
		while running_time() - self.start_time < GAME_LENGTH * 1000:
			self.move_basket()

	def finish(self):
		display.scroll("finish")
```

Flash the micro:bit and check that you can see the basket on the bottom row of LEDs. It should move left and right when you press the buttons but it should not disappear off the edge of the display. After 20 seconds, the game will end with the “finish” message.



## 5. Add one egg

Next add the definition of the `Egg` class. It has methods to show and hide the egg, similar to the methods for the Basket. The `move_down()` method changes the y coordinate of the egg on the display.

The game code will need to know if the egg has been caught in the basket or has reached the ground. The methods `is_caught()` and `is_smashed()` will return `True` or `False`. Work through the logic inside these methods to make sure you understand what’s happening.

> Add this code just before the `EggGame` class. 


```python
class Egg:

	def __init__(self, x):
		self.x = x
		self.y = EGG_START_Y

	def show(self):
		try:
			display.set_pixel(self.x, self.y, EGG_BRIGHTNESS)
		except ValueError:
			pass

	def hide(self):
		display.set_pixel(self.x, self.y, OFF_BRIGHTNESS)

	def move_down(self):
		self.y += 1

	def is_smashed(self):
		return (self.y > MAX_Y)

	def is_caught(self, basket_x):
		return ((self.y == MAX_Y) and (self.x == basket_x))
```

With the `Egg` class written, you can use its methods in the game code. Add the code below to the `EggGame` code.

There will be many eggs dropping at the same time. Each egg will be a separate object instance of the `Egg` class. To keep track of the eggs, we will use a Python list to hold the instances.

The statement `self.eggs = []` sets up an empty list when the game starts.

The statement `self.eggs.append(Egg(random.randint(MIN_X, MAX_X)))` creates a new instance of `Egg` at a random position on the top row of LEDs and adds it to the list.

Make sure you understand how the `show_eggs()` and `hide_eggs()` methods work.

> Add this code to `EggGame` immediatley after the ` __init__()` method. Make sure you indent it correctly to line up with the other methods.


```python
	def show_eggs(self):
		for egg in self.eggs:
			egg.show()
	
	def hide_eggs(self):
		for egg in self.eggs:
			egg.hide()

	def drop_egg(self):
		self.eggs.append(Egg(random.randint(MIN_X, MAX_X)))
```

Now change the ``__init__()`` method so that it looks exactly like the code below.

```python
class EggGame:

	def __init__(self):
		self.basket = Basket()
		self.eggs = []
		self.start_time = 0
		self.start()
		self.play()
		self.finish()
```

Finally add two more statements to the start() method. This will drop the first egg and display it.

```python
	def start(self):
    	self.start_time = running_time()
		self.drop_egg()
		self.show_eggs()
		self.basket.show()
```

Flash the micro:bit and check that, as well as the basket, you can see one egg in a random position on the top row of LEDs. Press the micro:bit reset button a few times to see where the egg appears.



##6. Let the eggs rain down

With one egg working, you can now add the code to handle many eggs at once, and make them drop. 

The `sweep_up_eggs()` and `caught_egg()` methods use a powerful Python feature called a **list comprehension**. Ask your mentor to explain how it works.

> Add this code to `EggGame` immediatley after the drop_egg` ()` method. Make sure you indent it correctly to line up with the other methods.

```python
	def move_eggs(self):
		for egg in self.eggs:
			egg.move_down()

	def sweep_up_eggs(self):
		self.eggs[:] = [egg for egg in self.eggs if not (egg.is_smashed() or egg.is_caught(self.basket.x))]

	def caught_egg(self):
		return [egg for egg in self.eggs if egg.is_caught(self.basket.x)]
```

Now change the ``__init__()`` method so that it looks exactly like the code below. This sets up the scoring and the “clock” that will control how fast the eggs move.

```python
class EggGame:

	def __init__(self):
		self.basket = Basket()
		self.eggs = []
		self.start_time = 0
		self.last_tick = 0
		self.score = 0
		self.start()
		self.play()
		self.finish()
```

Finally, change the `start()` , `play()` and `finish()` methods as shown below.

Work through the logic inside the `play()` method to make sure you understand what’s happening.

```python
	def start(self):
		self.start_time = running_time()
		self.last_tick = self.start_time
		self.drop_egg()
		self.show_eggs()
		self.basket.show()

	def play(self):
		while running_time() - self.start_time < GAME_LENGTH * 1000:
			self.move_basket()
			if running_time() - self.last_tick > TICK:
				self.last_tick += TICK
				self.hide_eggs()
				self.move_eggs()
				if self.caught_egg():
					self.score += 1	
				self.drop_egg()
				self.sweep_up_eggs()
				self.show_eggs()
	
	def finish(self):
		display.scroll("Score: {} eggs".format(str(self.score)), 100)
```

Flash the micro:bit and play the game. See how many eggs you can catch in the game time. Check that the score is displayed correctly.



##7. What next?

Well done! You have the basic It’s Raining Eggs game working. How could you improve the game? Here are some ideas:

-   Speed up the rate at which the eggs drop - this is an easy change :-)

-   Change the scoring so that you lose 1 for each smashed egg.

-   Tilt the micro:bit left and right to move the basket, instead of using the buttons.

-   Tilt the micro:bit forward and backwards to speed up or slow down the rate at which the eggs drop.

-   Drop more than one egg at a time – this needs changes to the scoring code as well as the “dropping eggs” code

-   Use radio to turn it into a multi-player game: one player presses a button to start, then all players see a synchronised countdown timer.

Try adding some of these features. Ask your mentor for help if you need it.
