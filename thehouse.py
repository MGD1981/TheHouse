from sys import exit
from random import randint


# Room Numbers:
# 0 = 'outside', 1 = 'foyer', 2 = 'library', 3 = 'kitchen',
# 4 = 'dining_room', 5 = 'basement', 6 = 'upstairs', 7 ='vault'


# Asks user to enter a number, returns an integer.
def choose():
    selection = (raw_input("Please choose: ")) 
    try:
        selection = int(selection)
    except ValueError:
        None
    return selection

# Shows inventory list, returns user-chosen member or 'nothing'.
def use_item():
    active = True
    while active:
        print "\nYou currently possess the following:"
        print ', '.join(inventory)
        print "\nWhat would you like to use?  Enter 'nothing' to go back."
        item = raw_input("=> ")
        if not item in inventory and item != 'nothing':
            raw_input("\nYou don't have that.")
        else:
            active = False
            return item       

# Prints fail message if used item has no function in room.
def item_fail(self):
    print "\nYou try to use the %s, but it doesn't" % self,
    raw_input("do anything here.")
    
# Combat function, taking 'enemy name' and 'enemy hitpoints' as
# parameters.  Player hitpoints set randomly between 3-5.  Each
# strike does 1-5 damage.
def melee(self, enemy_hp):
    your_hp = randint(3,7)
    print "\nYou are grappling with a %s!" % self
    feeling = ['lousy', 'alright', 'fine', 'pretty good', 'very good']
    raw_input("\nYou are feeling %s: %d hitpoints." 
              % (feeling[your_hp - 3], your_hp)) 
    while True:
        print "\nYou have %d hitpoints remaining." % your_hp
        print "The %s has %d hitpoints remaining." % (self, enemy_hp)
        print "\nWhat would you like to do?"
        print "1) Punch it!"
        print "2) Cry."
        choice = choose()
        if choice == 1:
            raw_input("\nYou punch the %s!" % self)
            enemy_hp -= randint(1,5)
            if enemy_hp <= 0:
                return('win')
            raw_input("\nThe %s strikes you!" % self)
            your_hp -= randint(1,5)
            if your_hp <= 0:
                return('lose')
        elif choice == 2:
            raw_input("\nYour tears have no effect on the %s!" % self)
            raw_input("\nThe %s punches you!" % self)
            your_hp -= randint(1,5)
            if your_hp <= 0:
                return('lose')
        else:
            raw_input("\nI don't understand that command.") 
    

class Play(object):

    def __init__(self, room_num):
        self.room_num = room_num
    
# This function is a misnomer; it runs only once, and then in an infinite loop
# until an exit command.  The loop runs 'enter' function after 'enter'
# function on the returned integers which correspond to the 'room_list'
# list, which in turn corresponds to the class library below.
# i.e. function loops 'Class(Room)'.enter, and each of those classes
# either exits or returns another room.
    def new_room(self):
        room_class = {
            'outside': Outside(),
            'foyer': Foyer(),
            'library': Library(),
            'kitchen': Kitchen(),
            'dining_room': DiningRoom(),
            'basement': Basement(),
            'upstairs': Upstairs(),
            'vault': Vault()
            }
        
        next_room = self.room_num
        
        while True:
            next_room = room_class[room_list[next_room]].enter()



class Room(object):
    
    def __init__(self):
        pass

class Outside(Room):
    
    def __init__(self):
        pass
        
    def enter(self):
        print "\nYou are outside.  The sun is shining."
        print "There is a door to a large house to the north."
        if not 'flower' in inventory:
            print "There is a flower here."
        print "\nWould you like to:"
        print "1) Go inside"
        print "2) Spontaneously combust"
        print "3) Use an item."
        if not 'flower' in inventory:
            print "4) Take the flower."
        choice = choose()
        if choice == 1:
            return 1
        elif choice == 2:
            print "\nYou explode.  Guts are everywhere.\n"
            exit(1)
        elif choice == 3:
            item_used = use_item()
            if item_used == 'flower':
                raw_input("\nYou put the flower back where you found it.")
                inventory.remove('flower')
                return 0
            else:
                item_fail(item_used)
                return 0
        elif choice == 4 and not 'flower' in inventory:
            raw_input("\nYou take the flower.")
            inventory.append('flower')
            return 0
        else:
            return 0

class Foyer(Room):
    
    def __init__(self):
        pass
        
    def enter(self):
        print "\nYou are in the foyer."
        print "To the west is a library, and to the east is a kitchen."
        print "There is a staircase leading upwards in front of you."
        print "\nWould you like to:"
        print "1) Go back outside."
        print "2) Enter the library."
        print "3) Enter the kitchen."
        print "4) Go upstairs."
        print "5) Use an item."
        choice = choose()
        if choice == 1:
            return 0
        elif choice == 2:
            return 2
        elif choice == 3:
            return 3
        elif choice == 4:
            return 6
        elif choice == 5:
            item_used = use_item()
            item_fail(item_used)
            return 1
        else:
            return 1
        
class Library(Room):

    def __init__(self):
        self.books_searched = False
        self.door_found = False
        pass
    
    def enter(self):
        print "\nYou are in a small library."
        print "There is a door to the dining room to the north, and an entrance"
        print "to the foyer.  A cozy fire burns in the fireplace."
        if not self.books_searched:
            print "You see a great many books."
        elif self.door_found:
            print "There is a tunnel leading to the basement."
        else:
            print "You see a great many books, including a Python manual."
        print "\nWould you like to:"
        print "1) Enter the foyer."
        print "2) Enter the dining room."
        if not self.books_searched:
            print "3) Read some books."
        elif self.door_found:
            print "3) Enter the basement."
        else:
            print "3) Take the Python book."
        print "4) Use an item."
        choice = choose()
        if choice == 1:
            return 1
        elif choice == 2:
            return 4
        elif choice == 3 and not self.books_searched:
            print "\nAmidst the collection of great novels, you come across a leather bound"
            raw_input("edition of a Python programming manual.")
            self.books_searched = True
            return 2
        elif choice == 3 and self.books_searched and not self.door_found:
            print "\nYou grab the book and attempt to pull it off of the shelf, triggering"
            print "a mechanism which rotates the bookcase ninety degrees, revealing"
            raw_input("an entrance to the basement.")                 
            self.door_found = True
            return 2
        elif choice == 3 and self.door_found:
            return 5
        elif choice == 4:
            item_used = use_item()
            if item_used == 'candle':
                inventory.remove('candle')
                inventory.append('lit candle')
                raw_input("\nYou light the candle in the fireplace.")
            else:
                item_fail(item_used)
            return 2
        else:
            return 2
        
class Kitchen(Room):

    def __init__(self):
        self.cheese_monster = True
        pass
    
    def enter(self):
        print "\nYou are in a messy kitchen.  There is a dining room the the north,"
        print "and the foyer to the south."
        print "There is food splattered everywhere."
        if self.cheese_monster:
            print "An awful smell emanates from the refrigerator."
        print "\nWould you like to:"
        print "1) Enter the dining room."
        print "2) Enter the foyer."
        print "3) Open the refigerator."
        print "4) Use an item."
        choice = choose()
        if choice == 1:
            return 4
        elif choice == 2:
            return 1
        elif choice == 3:
            if not self.cheese_monster:
                raw_input("\nNo way, it's awful in there!")
                return 3
            else:
                raw_input("\nYou open the door to an overpowering stench...")
                raw_input("\nSuddenly, from inside the refrigerator, something lunges at you!...")
                # Rough odds of winning: 8 to 2
                fight_result = melee('Cheese Monster', randint(3, 5))
                self.cheese_monster = False
                if fight_result == 'win':
                    print "\nYou are victorious!!"
                    raw_input("\nYou take some cheese as a reward.")
                    inventory.append('cheese')
                    return 3
                else:
                    print "\nThe Cheese Monster knocks you unconscious and uses you as"
                    raw_input("a host organism for its offspring.")
                    print "\nYou wake up with an awful stomach ache."
                    inventory.append('cheese monster larva')
                    raw_input("\nThe monster is nowhere to be found.")
                    return 3
        elif choice == 4:
            item_used = use_item()
            item_fail(item_used)
            return 3
        else:
            return 3
        
class DiningRoom(Room):

    def __init__(self):
        pass
        
    def enter(self):
        print "\nYou are in a grand dining room with crystal chandeliers."
        print "A long oaken table is set with fine china and silver candlesticks."
        print "To the south are doors to the kitchen and the library."
        print "\nWould you like to:"
        print "1) Enter the kitchen."
        print "2) Enter the library."
        if (not 'candle' in inventory) or (
                not 'lit candle') in inventory:
            print "3) Take a candlestick."
            print "4) Use an item."
        else:
            print "3) Use an item."
        choice = choose()
        if choice == 1:
            return 3
        elif choice == 2:
            return 2
        elif choice == 3 and ((not 'candle' in inventory) and (
                not 'lit candle' in inventory)):
            inventory.append('candle')
            raw_input("\nThe candlestick is too heavy and awkward, but you take the candle.")
            return 4
        elif choice == 3 or (choice == 4 and not((
                 'candle' in inventory) or ('lit candle' in inventory))):
            item_used = use_item()
            item_fail(item_used)
            return 4
        else:
            return 4


class Basement(Room):

    def __init__(self):
        self.clown = True
        self.clown_searched = False
        pass
        
    def enter(self):
        if not 'lit candle' in inventory:
            print "\nThis room is pitch black.  You cannot see anything."
            print "\nWould you like to:"
            print "1) Backtrack to the library."
            print "2) Boldly venture forward."
        else:
            print "\nBy candlelight, you make out your cavernous surroundings."
            print "There is a large vault door to the west, padlocked."
            if self.clown:
                print "A clown licking a butcher knife reclines idly next to the door."
            else:
                print "The body of a dead clown with a big knife slumps in the corner."
            print "\nWould you like to:"
            print "1) Return to the library."
            print "2) Enter the vault."
            if self.clown:
                print "3) Fight the clown."
            else:
                print "3) Search the clown's corpse."
            print "4) Use an item."
        choice = choose()
        if (choice != 1 and choice != 2) and not 'lit candle' in inventory:
            return 5
        if choice == 1:
            return 2
        elif choice == 2 and 'lit candle' in inventory:
            if 'key' in inventory:
                raw_input("\nThe key fits the padlock!")
                inventory.remove('key')
                raw_input("\nAs you enter the vault, the door slams shut behind you.")
                return 7
            else:
                raw_input("\nThe door is locked.")
                return 5
        elif choice == 2 and not 'lit candle' in inventory:
            raw_input("\nA clown stabs you and eats your heart.\n")
            raw_input("That was a really stupid decision.\n")
            exit(1)
        elif choice == 3 and self.clown:
            raw_input("\nYou lunge wildly, flailing your fists.")
            # Rough odds of winning: 3 to 7
            fight_result = melee('clown', randint(7, 10))
            if fight_result == 'lose':
                raw_input("\nWhat a surprise.  The knife-wielding clown killed you.\n")
                exit(1)
            else:
                self.clown = False
                raw_input("\nYou have successfully murdered a clown.")
                return 5
        elif choice == 3 and not self.clown:
            raw_input("\nThe butcher knife appears to be welded to the clown's hand.")
            if not self.clown_searched:
                self.clown_searched = True
                inventory.append('key')
                raw_input("\nOoh!  There's a key in his mouth!  You take it.")
            return 5
        elif choice == 4:
            item_used = use_item()
            if item_used == 'key':
                raw_input("\nPretty sure this will fit in the padlock on the vault door!")
            elif (item_used == 'flower') and self.clown:
                raw_input("\nYou smile at the clown and offer him the pretty flower.")
                raw_input("\nCurious, the clown takes it from your hand and brings it to his nose.")
                inventory.remove('flower')
                print "\nIn his attempt to smell the flower, the clown accidentally stabs"
                raw_input("himself in the face.")
                self.clown = False
            else:
                item_fail(item_used)
            return 5
            
            
class Upstairs(Room):

    def __init__(self):
        pass

    def enter(self):
        print "\nYou are in a bedroom."
        print "There is a bed."
        print "There is also a dresser and a nightstand."
        print "\nWould you like to:"
        print "1) Go downstairs."
        print "2) Search the furniture."
        print "3) Use an item."
        choice = choose()
        if choice == 1:
            return 1
        elif choice == 2:
            if 'vitamins' in inventory:
                raw_input("\nYou find nothing of further interest.")
            else:
                print "\nThe dresser is filled with moth-eaten rags and a couple of paper"
                print "party-hats with broken elastic.  The bed looks like it hasn't been slept on"
                print "in a long time."
                raw_input("\nYou find a bottle of vitamins in the nightstand.  You take it.")
                inventory.append('vitamins')
            return 6
        elif choice == 3:
            item_used = use_item()
            item_fail(item_used)
            return 6
        else:
            return 6


class Vault():

    def __init__(self):
        self.mouse = True
        pass
        
    def enter(self):
        print "\nThe room is small, and lined with steel.  Flourescent lights buzz overhead."
        print "\nIn the middle of the floor lies an ornate treasure chest."
        print "A brass wire cage hangs from the ceiling.  The cage door is open."
        print "There is a gray mouse inside the cage."
        print "\nWould you like to:"
        print "1) Leave the vault."
        print "2) Open the chest."
        if self.mouse:
            print "3) Fight mouse."
        else:
            print "3) Fight dead mouse."
        print "4) Use an item."
        choice = choose()
        if choice == 1:
            raw_input("\nThe door is locked!")
            return 7
        elif choice == 2 and self.mouse:
            raw_input("\nYou approach the chest and place your hands on the lid.")
            raw_input("\nSuddenly, the little gray mouse jumps down and rips out your neck.")
            raw_input("\nNever underestimate the mouse.\n")
            exit(1)
        elif choice == 2 and not self.mouse:
            raw_input("\nYou approach the chest and place your hands on the lid.")
            raw_input("\nWith great caution, you slowly open the heavy container.")
            raw_input("\nOh..."),
            raw_input("my God...")
            raw_input("\nThe chest is filled with gold and precious gems!!")
            print "\nFinding a key to the vault in the bottom of the chest, you open the door"
            print "and drag your newfound riches back up through the house."
            raw_input("\nYou step outside and take a breath of fresh air.")
            print"\nCongratulations!  Another profitable home invasion!"
            raw_input("You've won the game!!\n")
            exit(1)
        elif choice == 3 and self.mouse:
            print "\nAre you sure?  This mouse is very strong."
            print "1) Yes, I'm sure.  I can beat a mouse, thanks."
            print "2) Uh... okay, I guess I'll reconsider."
            choice = choose()
            if choice == 1:
                raw_input("\nYou approach the cage menacingly.")
                # Rough odds of winning: 1 to 199
                fight_result = melee('little gray mouse', randint(15, 20))
                if fight_result == 'lose':
                    raw_input("\nYou are dead.  The mouse killed you.")
                    raw_input("\nI warned you.  Some people never listen.\n")
                    exit (1)
                else:
                    self.mouse = False
                    raw_input("\nYou did it!  You have obliterated the little gray mouse!")
                    return 7
            else:
                return 7
        elif choice == 3 and not self.mouse:
            raw_input("\nYou play with the dead mouse.  Creep.")
            return 7
        elif choice == 4:
            item_used = use_item()
            if item_used == 'cheese' and self.mouse:
                raw_input("You feed your cheese to the mouse.  He seems to enjoy it.")
                inventory.remove('cheese')
                return 7
            elif item_used == 'vitamins' and (
                    self.mouse and 'cheese monster larva' in inventory):
                raw_input("\nYou swallow the vitamins and feel much stronger!")
                inventory.remove('vitamins')
                raw_input("\nWait... actually... now your stomach kind of hurts.")
                raw_input("\nUuuugggghhhh oooooooooohh...")
                raw_input("\nUuuaaaaaaAAAHHHH!!  PAIN!!  PAAAINNN!!!")
                raw_input("\nSuddenly, a baby Cheese Monster bursts out of your chest!")
                inventory.remove('cheese monster larva')
                raw_input("\nThe baby Cheese Monster leaps at the little gray mouse and swallows it whole!")
                self.mouse = False
                print "\nThe baby Cheese Monster winks at you knowingly, and then vanishes"
                raw_input("through a small hole in the ceiling.")
                raw_input("\nYou actually feel pretty okay.")
                return 7
            else:
                item_fail(item_used)
                return 7
        else:
            return 7

# Could this list be moved to the Play.new_room() definition?
room_list = ['outside', 'foyer', 'library', 'kitchen',
             'dining_room', 'basement', 'upstairs', 'vault']

# Inventory list starts with nothing.
inventory = []

start = Play(0)
start.new_room()
