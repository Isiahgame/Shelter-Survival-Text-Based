#Text-based Fallout Shelter game developed by T.G. and The-9880
from random import randint
from operator import attrgetter #Used to sort objects by a chosen attribute

class human(object): #Basic class for all the humans present in the game.
	def __init__(self,name,day_of_birth,parent_1,parent_2,gender):
		if len(all_people) <6 and day_count<3: #First 5 people will be 21 years old, so they can mate.
			self.age=21
		else:
			self.age=0
		self.assigned_room=[] #Keeps track of where person is working.
		self.hunger=0
		self.thirst=0
		self.name = name
		self.parent_1=parent_1
		self.parent_2=parent_2
		self.gender=gender[0].lower()
		self.scavenging = 0
		self.daysScavenging = 0
		self.daysToScavengeFor = 0
		self.HP=100
		#The stats of the person. Plan to use this to affect the production of room the person has been assigned to.
		self.strength=1
		self.perception=1
		self.endurance=1
		self.charisma=1
		self.intelligence=1
		self.luck=1
		
		self.can_mate=0 #Keeps track of mating ablility
		self.children=[] #List of all children
		self.partner="" #Keeps track of partner of person. Only partners can have coitus.
		
		
	def mature(self):
		self.age+=1
		print(self.name," has matured and is now ",self.age," years old!")
	def rebirth(self): #Don't know if I'll ever use this.
		self.age=0
		if self.gender=="f":	
			print(self.name," has been reborn and his stats have been reset")
		else:
			print(self.name," has been reborn and her stats have been reset")
		self.strength=1
		self.perception=1
		self.endurance=1
		self.charisma=1
		self.intelligence=1
		self.luck=1
		self.assigned=0 #Keeps track of whether or not human has been assigned to a room.
		
	def assign_to_room(self,chosen_room):
		global rooms
		global all_people
		if not check_room(chosen_room):
			print("Error with room allocation system. Please contact dev.")
		else:
			del(all_people(self).assigned_room][:])  #Clears the variable that holds the room the character has been assigned to.
			all_people(self).assigned_room.append(str(chosen_room)) #Lets the character know where they've been assigned.
			
			for x in range(all_people): #Fetches the index of the person being assigned.
				if all_people[x].name==self.name:
					index=x
					break
			rooms(chosen_room).inhabitants[index]=1 #Let's room know this person has been assigned to the room
			
	def can_mate_check(self): #Checks if person can have coitus and have children. Perfomed twice when player inputs coitus, once for each proposed parent.
		self.can_mate=1
		if self.age <18:
			self.can_mate=0
		if len(self.children)>5: #Upper limit of children is 5
			self.can_mate=0
		for child in self.children: #Have to wait for a year before parent can have child again.
			if all_people(child).age<1:
				self.can_mate=0
	def die(self): 
		global end
		global all_people
		global rooms
		print(self.name," has died")
		if all_people[0].name==self.name: #Uses first index since player will always be the first person in the list, checks if player has died.
			end=1 #Ends game since player has died.
		if self.assigned_room!="": #Deals with if the person was assigned to any rooms.
			for x in range(all_people): #Fetches the index of the person.
					if all_people[x].name==self.name:
						index=x
						break
			for r in rooms:
				del r.assigned[index] #Removes person from the rooms' assigned records.
		all_people.remove(self)
		
		
		
class room(object): #Basic class for the rooms in the game.
	def __init__(self,name): #Name would be something like "living_room_3" while group would be "living". So all living rooms have the same initial stats.
		self.name=name 
		self.assigned=0 #1s and 0s that are used to store the indexes of inhabitants. Eg 001001 means that the 3rd and the 6th characters have been assigned here.
		self.level=1 #Determines production level, max inhabitants.
		if self.name=="living": # Living rooms have no "inhabitants". Number of living rooms just limits the total population of the shelter.
			self.risk=0
			self.can_produce=0 #Stores whether or not room actually produces anything.				self.components=["wood",] #Need to add components.
		elif self.name=="generator":
			self.can_produce=1
			self.inhabitants_limit=5 #Max number of workers that can work in the room at one time.
		elif self.name=="storage":
			self.can_produce=0
			self.inhabitants_limit=0 #Max number of workers that can work in the room at one time.
		elif self.name=="kitchen":
			self.can_produce=1
			self.inhabitants_limit=0 #Max number of workers that can work in the room at one time.
		elif self.name=="trader":
			self.can_produce=0
			self.inhabitancts_limit=1
		else:	
			print("Bug with room creation system. Please contact dev. Class specific bug.")
		if self.can_produce==1:
			self.production=100
			self.can_rush=1
		# Need to add more names.	
		
	def rush(self): 
		global rooms
		if self.can_rush==0: #Method should never be called on non-rushable rooms.
			print("Bug with can_rush check. Please contact dev.")
		else:
			self.production+=50
			self.rushed=1 #Lets game know this room has been rushed.

	def update_assigment(): #Updates length of assigned variable by adding more zeros to it.
		global rooms
		current_count=len(self.assigned)
		required_count=len(all_people)
		if current_count<required_count:
			difference=required_count-current_count
			for x in range(difference):
				self.assigned.append(0) #Adds a zero at the end of the string based on the total population.
		
	def update_production(self): #Calculates production level based on number of and skills of inhabitants. 
	#Maybe get the sum of all the inhabitants stats, depending on the room group. E.g. a generator's production may be based on the strength of the workers.
		global rooms
		if self.can_produce==0:
			print("Bug with room production update system. Please contact dev")
		else:
			total_stat=0 
			if self.group=="generator":
				for name in self.inhabitants:
					total_stat+=all_people(name).intelligence
			elif self.group=="kitchen":
				for name in self.inhabitants:
					total_stat+=all_people(name).charisma
			#Add more cases for all rooms that can produce
			else:
				print("Bug with room production update system. Please contact dev")
			rooms(self).production+=total_stat
			
	def upgrade(self):
		global rooms
		if self.can_produce==1:
			self.production+=20
			self.inhabitants_limit+=2
			self.level+=1
	def count_component(self,component):
		count = 0
		for x in self.components:
			if x == component:
				count += 1
		return count
	
	
class item(object): # Basic model for items in the game. Objects of this class will never be stored.
	def __init__(self,name):
		self.name=name#Just needs to get the name, all other attributes are automatically assigned by the following lines.
		if self.name=="wood":
			self.value=10
			self.weight=5
			self.components=[] #This is a basic item and cannot be scrapped.
			self.rarity=1 #Determines chance of it showing up during scavenging or in the trader's inventory
		elif self.name=="steel":
	    	self.value=10 	
	    	self.weight=5 
	    	self.components=[]
	        self.rarity=2
	    elif self.name=="turret":
	    	self.value==200
	    	self.weight=20
	    	self.components=["steel","steel","steel","electronic chip"]
	        self.rarity=5
	    	
	    #Add special cases for every item that can exist in the game
	    else:
	    	print("Item doesn't exist. Bug with item creation system. Please contact dev.")
	    self.scrapped=0 #Keeps track of whether item has been scrapped by player.
	    
	def count_component(self,component):
		count = 0
		for x in self.components:
			if x == component:
				count += 1
		return count
		
	def scrap(self): #Destroys the item and adds it's compoenents to the inventory.
		global inventory
		print(self.name," has been scrapped and these")
		for item in self.components:
			inventory.append(item)
			print(item)
		print("have been added to your inventory")
		self.scrapped=1 #Differentiate between whether item has been scrapped or just destroyed
		self.destroy()
	
	def destroy(self):
		global inventory
		inventory.remove(self.name)
		if self.scrapped!=1: #Don't need to print anything if the item has been scrapped
			print(self.name," has been destroyed!")





#Information system!
# Bunch of functions used by other functions to retrieve information about the shelter, it's inhabitants, rooms and items.

def input_int(x): #Whenever player has to input an integer, this should be used. Catches errors.
	x=input("Input an integer.")
	try:
		int(x)
	else ValueError:
		print("Invalid. Only integer numbers are accepted!")
		x=input("Try again. Input:")
		check_int(x) #Recursion!
	return x


def count_item(item,target_inventory): #Counts total number of an item present in an inventory
	item=str(item)
	count=0
	if target_inventory=="player":
		for x in inventory:
			if x==item:
				count+=1
		return count
	elif target_inventory=="trader":
		for x in trader_inventory:
			if x==item:
				count+=1
		return count
	else:
		print("Bug with item counting system. Please contact dev!")
		
def count_weight(): #Calculates the sum of the weights of all items currently in the inventory,
	count=0
	for x in inventory:
		count+=item(x).weight #Creates instances of class on the fly. If 5 wood present, tempoarily creates 5 wood, one by one, uses their weight and discards them
	return count
		
def storage_capacity(): #Calculates how much more weight the player can hold.  Used to check if player can take any more items.
	global all_rooms
	capacity=all_rooms("storage").production
	return capacity
		
def check_room(x): #Checks if the room has been built yet	
	for r in all_rooms:
		if x==r.name:
			return True
	else:
		return False
		
def see_people(): #Displays everyone in the shelter.
	for person in all_people:
		print(person.name,person.age,person.gender,person.hunger,person.thirst) #Need to add more attributes

def see_rooms():
	all_rooms.sort(key=operator.attrgetter("name"))
	for r in all_rooms:
		print(r.name,". Risk: ",r.risk,". Inhabitants: ",r.inhabitants,". Level: ", self.level)
		
def see_inventory(inven):#Displays all items in inventory in the form (Log*5.Weight=5.Value=10.Components="Wood". Rarity=1).
	inven=str(inven)
	if inven=="player":
		for x in inventory:
			count=count_item(x,"player")
			if count>0: #If there are no instances of the item present, no need to display it.				
				it=item(x) #Creates a tempoary object so it's data can be fetched.
				print(x,"*",count,". Weight: ",it.weight,". Value: ",it.value,". Components: ",it.components,". Rarity: ",it.rarity)

	elif inven=="trader":
		for x in trader_inventory:
			count=count_item(x,"trader")
			if count>0: #If there are no instances of the item present, no need to display it.				
				it=item(x)
				if it.components!=[]
					print(x,"*",count,". Weight: ",it.weight,". Value: ",it.value,". Components: ",it.components,". Rarity: ",it.rarity)
				else:
					print(x,"*",count,". Weight: ",it.weight,". Value: ",it.value,". Components: ",it.components,". Rarity: ",it.rarity)
	else:
		print("Major bug with inventory information system. Please contact dev!")
def see_resources():
	food_count=count_item("food","player")
	water_count=count_item("water","player")
	power_count=count_item("watt","player")
	print("Food: ",food_count)
	print("Water: ",water_count)
	print("Power: ",power_count)
	






#Scavenging system.
def scavenge(person,var): #Sends people on a scavenging mission. Needs work.
	global all_people
	if person not in all_people:
		print("Error with scavenging system. Please contact dev!")
	else:
		all_people[person].scavenging=1
		if var=="days": #If player chooses to send player for certain number of days, or until health drops below 20.
			print("How many days do you want to send this person out?")
			day_choice=input_int()
			self.daysToScavengeFor = day_choice 
		else:
			self.daysToScavengeFor= 100 #Their health will drop below 20 before 100 days, so this is fine.


	
	
	
	

#Construction system.
def build(r): #Builds a room once checks are done. Should append to (rooms) list.
	global rooms
	global inventory
	built_room=room(str(r)) #creates a room. 
	rooms.append(built_room) #Stores the room in memory.
	for y in built_room.components: #Does this for each component
		for x in inventory: 
			if y == x: #If it matches, delete this.
				del(x) 
				break #Ensures that only one instance of the item is removed for every one instance of the component.
	
def craft(x):#Crafts an item once checks are done. Just add the name of an item to the inventory name.
	global inventory
	add_to_inven(x, 1, "player")
	a = item(x)
	for y in a.components:
		for x in inventory:
			if y == x:
				del(x)
				break #Ensures that only one instance of the item is removed.
	
	







#Human management system
def get_player_gender():#Asks player what gender they are.
	gender=input("Please choose a gender.(M/F)")
	gender=gender[0].lower()
	if gender=="m" or "f":
		return gender
	else:
		print("Invalid gender choice!")
		get_player_gender()
	
	
def get_gender(): #Randomly generates a gender. For NPCs
	gender=randint(0,1):
	if gender==0:
		gender="m"
	else:
		gender="f"
	return gender

def birth(parent_1,parent_2): #Creates new NPC.
	global all_people
	global rooms
	name=input("Choose a first name for the new child: ")
	if len(name.split())!=1:
		print("You have to input a single word!")
		birth(parent_1,parent_2)
	
	first_letter=name[0].upper()
	name=name[1,len(name))
	name=str(first_letter+name)
	all_people.append(human(name,day_count,parent_1,parent_2,get_gender()))
	all_people(parent_1).children.append(str(name))
	all_people(parent_2).children.append(str(name))
	all_people(parent_1).partner=str(parent_2)
	all_people(parent_1).partner=str(parent_2)
	for r in all_rooms:
		r.update_assigment()
	if day_count>2: #First few births cost no points
		use_points(50)
		
def first_four(): #Runs once at beginning of game. Creates 4 new people. Costs no Action Points!
	global all_people
	names=["Thompson","Elenor","Codsworth","Sharmak","Luthor","Marhsall","Cole","Diven","Davenport"] #Random surnames for inital 5 inhabitants. All children will inherit their surnames from their parents.	if day_count<2: #Initial 5 inhabitants need to be birthed
	while len(all_people)<6:
		num_1=randint(len(names))
		num_2=randint(len(names))
		if num_1==num_2:
			continue
		birth(names[num_1],names[num_2]) #Passes random names to birth() function.

def create_player():#Only ran at start of game. First inhabitant of vault should be the player.
	global all_people
	name=input("Choose a first name for yourself: ")
	surname=input("Choose a surname for yourself: ")
	parent_1=input("What is the surname of your father?")
	parent_2=input("What is the surname of your mother?")
	all_people.append(human(name,day_count,parent_1,parent_2,get_player_gender)
	

 
 
 
 
 
 
 
 
 
#Inventory managment system!
def rand_item(target_inventory): #Randomly chooses an item and adds it to either the player's or the trader's inventory
	#Used daily with trader inventory, to randomize the items they have on sale.. Used with player inventory when scavenging mission is done.
	global inventory
	global trader_inventory
	#Following lines randomly choose an item, based on rarity
    num=randint(1,1024)
    lst=[2**a for a in range(0,11)]
    count=0
    for chance in lst:
        if num<chance:
            break
        count+=1
    rar=11-count #Determines the rarity of an item. 50% chance it's a level 10, 25% chance it's a level 9, 12.5% chance it's a level 8 and so on.
    possible_items=[]
    for x in all_items:
    	if item(x).rarity==rar: 
    		possible_items.append(x)
    number=randint(len(possible_items))
    actual_item=possible_items[number]
    #Following lines actually store the item in memory
	if target_inventory=="player":
		add_to_inven(actual_item,1,inventory)
		print("You have found a ", actual_item)
	elif target_inventory=="trader":
		add_to_inven(actual_item,1,trader_inventory)
	else:
		print("Bug with random item system. Please contact dev!")
		
def find_rand_item(inven,times): #Finds x items randomly and adds it to an inventory.
	for x in range(times):
		rand_item(inven)  # passes iven to rand_item function

def add_to_inven(x,number,inven): # Adds (x) (number) times to (inven) inventory. E.g. wood,5,player
	global trader_inventory
	global inventory
	x=str(x)
	inven=str(inven)
	if x not in all_items:
		print("Invalid item. Major bug with inventory adding system. Please contact dev") #Should never happen, since all checks should be done before this function is called.
	else:
		if inven=="player":
			for y in range(number):
				inventory.append(x)
		elif inven=="trader":
			for y in range(number):
				trader_inventory.append(x)

def lose_items(inven,number): #Randomly deletes multiple items from the target_inventory
	global inventory
	global trader_inventory
	if iven=="trader": #Runs daily. Simulates trader selling some items to NPCs.
		for x in range(number):
			rand_number=randint(0,len(trader_inventory))
			inventory.remove(trader_inventory[rand_number])
	elif iven=="player": #Only runs when shelter has been raided by a hostile force.
		print("The raid made off with these items!")
		for x in range(number):
			rand_number=randint(0,len(inventory))
			e=iventory[rand_number]
			print(inventory[e])
			inventory.remove(e)
	else:
		print("Major bug in item losing system. Please contact dev!")
		

		



#Raiding system.
def raid(): 
	raiders=["Super Mutant","Raider","Synth","Feral Ghoul"]
	raider=raiders[randint(len(raiders))] #Randomly chooses a raider party.
	attack_power=randint(1,day_count//10)
	print("There was a ",raider," raid on your shelter!")	 
	if defense>attack_power:
		print("But your defenses were strong enough to send them packing!")
	else:
		loss=attack_power-defense
		lose_items("player",loss)
		if loss>10:
			death_chance=loss//10
			dice=randint(2,25):
			if death_chance<dice:
				#Death
				possible_deaths=all_people[1,len(all_people)-1] #The player can't die in a raid!
				death_number=randint(len(possible_deaths))
				print(possible_deaths[death_number]," has been killed in a raid")
				possible_deaths[death_number].die()
				
def update_defense(): #Updates the defense rating of the shelter, according to the presence of defensive items.
	global defense
	defense=0
	turret_count=count_item("turret","player")
	defense+=10*turret_count
		
	#Add cases for more items that increase defence	

	strength_sum=0
	for person in all_people:
		strength_sum+=person.strength
	defense+=strength_sum



#Happiness System.
def avg_hunger(): #Calculates average hunger level.
	total=0
	for x in all_people:
		total+=x.hunger
	avg=total/len(all_people)
	return avg
	
def avg_thirst(): #Calculates average thirst level
	total=0
	for x in all_people:
		total+=x.thirst
	avg=total/len(all_people)
	return avg

def feed(person,amount): #Reduces the hunger level of a person. 
#This needs to reduce the thirst level aswell.
	global all_people
	all_people(person).hunger-=amount
	if all_people(person).hunger<0:
		all_people(person).hunger=0
def drink(person,amount)
	global all_people
	all_people(person).thirst-=amount
	if all_people(person).hunger<0:
		all_people(person).thirst=0
def auto_feed():
	global all_people
	food_count=count_item("food","player")
	water_count=count_item("water","player")
	while food_count>0 and avg_hunger()>0:
		for person in all_people:
			feed(person,1)
			food_count-=1
	while water_count>0 and avg_thirst>0:
		for person in all_people:
			drink(person,1)
			water_count-=1
def happiness_loss(): #Depending on hunger or thirst level, reduces general happiness level.
	global happiness
	loss=0
	for y in range(30,101,10):
		if avg_hunger()<y:
			loss+=y-30
			break
	for y in range(30,101,10):
		if avg_thirst()<y:
			loss+=y-30 
			break
	if loss>0:
		happiness-=loss
		print("Due to your inhabitants being hungry and/or thirsty the shelter's overall happiness has dropped to ",happiness)


#Action Point usage system.
#This system is very important and needs to be developed.
#Should deduct from AP. If Ap gets below 0, stores the difference in (overuse). The next day's Action points should be less then.
#For example, if player has 10 action points left, and perfrom an action that costs 20, a day will pass but instead of 50, they'll have 40 action points
def use_points(point):
	global AP
	global overuse
	global overuse_amount
	if point>50:
		print("Bug with point usage system. It's trying to use 50, please note this and contact dev.")
	else:
		usage=AP-point
		overuse=0
		if usage<0: #If overuse occurs. i.e. if overuse is negative
			overuse_amount=0-usage
			overuse=1
		else: #If normal usage occurs. 
			AP=AP-usage
			

	

#Trading system.	
def trade(): #Trading system. Uses no Action Points
	global inventory
	global trader_inventory
	if "trader" not in built_room_types:
		print("There is no trader built. You can't trade until you set up a trading room.")
	else: # If trader exists, allows trading.
		while True: #"continue" lets trading continue, "break" stops trading
			print("Here are the traders' items: ")
			see_inventory("trader") 
			print("The trader has ", trader_caps, " caps.")
				
			print("Here are your items: ")
			see_inventory("player")
			print("You have ", caps, " caps.")
			
			print("For instance, input (buy 5 food) if you want to buy 5 units of food. Or input (end) to stop trading.")
			a=("What do you want to do?.")
			
			#Following lines are checks.
			if len(a)!=3:
				print("You have to input 3 words. Buy/sell,amount,item")
				continue
			try:
				int(a.split()[1])
			else ValueError:
				print("You have to input a number as the second word")
				continue
			if a.split()[2] not in all_items:
				print("Sorry. ",a.split()[2]," doesn't exist!")
				continue
			#Checks end here
			
			cost=item(all_items[a.split()[2]]).value #Fetches cost of item by tempoarily creating it's object and retreiving it's value attribute
			total_cost=cost*a.split()[1] #Sums up the money that is exchanging hands
			
			if a.split()[0]=="buy":
				if total_cost>caps:
					print("You can't afford that!")
					continue
				count=count_item(a.split(2),"trader")
				if a.split()[1]>count:
					if count==0:
						print("The trader doesn't have any ",a.split()[2])
					else:
						print("The trader doesn't have ",a.split()[1]," of ",a.split()[2])
					continue
				else:
					for x in range(a.split()[1]):
						trader_inventory[str(a.split()[2])].destroy()
						inventor.append(str(a.split()[2])
					caps-=total_cost
				continue
					
			elif action.split()[0]=="sell":
				if total_cost>trader_caps:
					print("The trader can't afford that!")
					continue
				count=count_item(a.split(2),"player")
				if a.split()[1]>count:
					if count==0:
						print("You don't have any ",a.split()[2])
					else:
						print("You don't have ",a.split()[1]," of ",a.split()[2])
					continue
				else:
					for x in range(a.split()[1]):
						_inventory[str(a.split()[2])].destroy()
						trader_inventory.append(str(a.split()[2])
					trader_caps-=total_cost
				continue
			
			elif action()[0]=="end":
				break
			
			else:
				print("Invalid Input! Try again!")
				continue
			
#Production system
def produce_all(): #Causes production of all rooms.
	global rooms
	global inventory
	for r in rooms:
		if r.can_produce==1:
			if r.name=="kitchen":
				for x in range(r.production//10):
					add_to_inven("food")
			elif r.name=="generator":
				for x in range(r.production//10):
					add_to_inven("watt")
			elif r.name=="water works":
				for x in range(r.production//10):
					add_to_inven("water")
			#Add more cases for each production capable room
			
				

	
#Choice system!
def choice():
	global auto_feed
	a=input("Choose what to do:")
	valid=1
	if a.split()[0]=="build": #Allows player to build new rooms. Checks if player has components to build room.
		if len(a.split())!=2:
			print("You have to input 2 words to build a room.")
		elif a.split()[1] not in all_rooms:
			print("This room doens't exist")
		elif a.split()[1] in rooms:
			print("You've already built this room")			
		else:
			can_build=1
			for ite in all_items:
				number_needed=rooms(a.split()[1]).count_component(ite)
				if number_needed>0:
					number_available=count_item(ite,"player")
					if number_needed>number_available:
						can_build=0
					else:
						print("You don't have enough ",ite, " to build a ",a.split()[1]
			if can_build==1:
				build(a.split()[1])
				
	elif a.split()[0]=="craft":
		#Checks to see if crafting possible.
		if a.split()[1] not in all_items:
			print("Invalid item. Try again.")
		else:
			can_craft=1
			actual_item = item(a.split()[1]) #Creates an instance of the item, so it's attributes can be fetched.
			for component in actual_item.components:
				number_available=count_item(component,"player")
				number_needed=actual_item.count_component(component)
				if number_needed>number_available: 
					print("You don't have enough ", x,"to craft ",y)
					can_craft=0
			if can_craft==1:
				print("You have crafted a ", a.split()[1]
				craft(a.split()[1])
			
	elif a.split()[0]=="rush":#Speeds up room tempoarily. Needs a lot of work. room.Rush() method incomplete.
		if a.split()[1] not in all_rooms:
			print("This room doesn't exist. Input (see rooms) to view all your rooms.")
		elif rooms(a.split()[1]).can_rush==0:
			print("This room cannot be rushed")
		else:
			a.split[1].rush()
		
	elif a.split()[0]=="see":
		if a.split()[1]=="people":
			see_people()
		elif (a.split()[1])[0,4]=="inven":
			see_inventory("player")
		elif a.split()[1]=="rooms":
			see_rooms()
		else:
			print("Incorrect input. To see people, input (see people). To view your inventory, input (see inventory) ")
		
		
	elif a.split()[0]=="coitus": #Allows player to create new inhabitants
		people_names=[a.name for a in all_people] #Used to check input
		if len(a)!=3:
			print("You need to input 2 mature people of opposite genders.")
			
		elif a.split()[1] not in people_names:
			print("No such",a.split()[1]," exists!")
			
		elif a.split()[2] not in people_names:
			print("No such",a.split()[2]," exists!")
		else:	
			person_1=all_people(a.split()[1]) #Refers to list of objects(Cuz people are objects. Nothing more!).
			person_2=all_people(a.split()[2])
			if (person_1.partner=="" and person_2.partner=="") or person_1.partner==person_2.name:			
				if person_1.age <18:
					print(a.split()[1]," isn't old enough to copulate.")					
				elif person_2.age <18:
					print(a.split()[2]," isn't old enough to copulate.")
				elif person_1.surname==person_2.surname:
					print("Sorry. Incest isn't allowed. At least be ethical!")
				elif person_1.gender==person_2.gender:
					print("The people need to be different genders! COME ON MAN CAN U EVEN BIOLOGY!")
				else:
					birth(person_1,person_2) #Pass these love birds to the birthing system
			else:	
				print("Infedility shall not be allowed!!!")
				print(person_1.name,"  is married to ",person_1.partner)
				print(person_2.name,"  is married to ",person_2.partner)
				
			
																												
	elif a.split()[0]=="feed": #Checks if player has enough food to feed person and then calls feed(person) function.
		food_count=count_item("food") #Counts how much food is available for feeding
		if avg_hunger()<2:
			print("You're people are working on full bellies boss!")
			
		elif len(a.split())==2: #If player wants to feed only one person
			if a.split()[1] not in all_people: #Checks if chosen human exists
				print("This person doesn't exist.")
			else:	
				hunger=all_people(a.split()[1].hunger) #Fetches hunger level of selected human
				amount=input("Feed ",a.split()[1],"  by how much?")
				if amount<hunger:
					print("You don't have enough food to feed ",a.split()[1])
				else:
					feed(a.split()[1],amount)
		else: 
			print("Invalid input! Can only feed one person like this. Use the auto_feed system to feed everyone.")
			
	elif a.split()[0]=="trade":
		if "trader" not in rooms:
			print("You haven't built a trader room yet!")
		elif rooms["trader"].inhabitants==[]:
			print("No one has been assigned to this room! You can't trade untill then.")
		else:
			trade()
			
	elif a.split()[0]=="see":
		if a.split()[1]=="people":
			see_people()
		elif a.split()[1][0,5]=="inven":
			see_inventory()
		elif a.split()[1]=="rooms":
			see_rooms()
		else:
			print("You choose see your (people), your (inven)tory or your (resources)")
			
			
	elif a.split()[0]=="assign":
		global all_people
		if len(a.split())!=4:
			print("You have to input 4 words. E.g. assign Thomas to living")
		elif a.split()[1] not in all_people:
			print("This ",a.split()[1]," doesn't exist."
		elif a.split()[3] not in all_rooms:
			print("This room doesn't exist.")
		elif a.split()[3] not in rooms:
			print("You haven't built this room yet")
		else:	
			all_people(a.split()[1]).assign_to_room(a.split()[3])
		
	elif a.split()[0]=="upgrade":
		global rooms
		if a.split()[1] not in rooms:
			print("This room doesn't exist. Try again.")
		elif a.split()[1]=="trader":
			print("This room cannot be upgraded")
		else:
			r=rooms(a.split()[1]) #Tempoarily fetches room so it's attributes can be used
			items_needed=r.components 
			for x in range(r.level-1): #The higher the level, the more components needed to upgrade
				items_needed=items_needed.append(items_needed)	
			can_up=1 #Can the room be upgraded or not?
			for ite in all_items: #For each item
				needed=0 #Counts how many are needed
				for comp in items_needed: 
					if ite==comp:
						needed+=1
				available=count_item(ite,"player") #Counts number of component available to the player
				if available<needed:
					can_up=0
					break
			if can_up==1:
				rooms(split()[1]).upgrade()
				
	elif a.split()[0]=="disable":
		if a.split()[1]=="auto feed":
			auto_feed=0
			print("Warning. You have disabled the auto_feed feature. Be careful, your people may starve!")
		else:
			print("Invalid input. You can disable the (auto_feed) system.")
			
	elif a.split()[0]=="enable":
		if a.split()[1]=="auto feed":
			auto_feed=1
			print("Auto-feed system is working optimally.")
		else:
			print("Invalid Input. You can enable the (auto_feed) system.")
			
	elif a.split()[0]=="scavenge":
		if a.split()[1] not in all_people:
			print("This person doesn't exist.")
		elif all_people(a.split()[1]).scavenging==1:
			print("This person is already out scavenging.")
		else:
			cho=input("Would you like to scavenge for a certain number of days or until their health gets low?(D/H)")
			cho=cho[0].lower()
			if cho=="d":
				scavenge(a.split()[1],"days")
			elif cho=="h":
				scavenge(a.split()[1],"")
			else:
				print("I'm just going to send them out until their health drops.")
				scavenge(a.split()[1],"")
	else:
		print("Invalid Input. Try again.")
		

	

#Game system.
def game():#Needs work
	global day_count
	global end
	global postition
	global inventory
	global rooms
	global caps
	global trader_inventory
	global trader_caps
	global defense
	global overuse
	global happiness
	global overuse
	global auto_feed
	global overuse_amount
	
	day_count=0
	end=0 #Can lose postition or die.  This is used for a while loop.
	print("Welcome to the text-based fallout shelter game!")
	print("Welcome, great Overseer!")
	print("It is your great duty to increase the population of your vault and keep your inhabitants happy.")
	create_player()
	player.age=20
	print("Commands: ")
	#Put Instructions for player here
	print("You have been given 100 caps to start your journey.")
	
	postition="secure" #Only changed to "lost" when happiness drops below 5.
	inventory=[] #All items that belong to the player. Just names
	all_items=["wood","steel","turret","food","water",] #Stores every possible item in the inventory. Just names.
	all_rooms=["living","bath","generator","kitchen","trader","storage",""] #Stores every possible room in the game. Just names.
	rooms=[] #Rooms that player has built. Objects!
	all_people=[] #All the people alive in the shelter. Objects!	
	caps=100
	trader_caps=400
	happiness=100
	trader_inventory=[]
	defense=0 
	overuse=0#Keeps track of whether or not player has used too many action points.
	auto_feed=1
	overuse=0
	
	while end==0 and position=="secure": #Loops the day
		AP=50
		if overuse==1:
			AP=50-overuse_amount
			
		print("Today is day ".day_count)
		
		for person in all_people: #Performs daily checks for all people.
			person.hunger+=10
			if person.hunger>99:
				print(person.name," has died of hunger")
				person.die()
			elif person.hunger>80:
				print("Warning!",person.name," is starving and may die soon.")
			elif person.hunger>50:
				print(person.name," is hungry.")
			person.thirst+=10
			if person.thirst>99:
				print(person.name," has died of thirst")
				person.die()
			elif person.hunger>80:
				print("Warning!",person.name," is extremely thirsty and may die soon.")
			elif person.hunger>50:
				print(person.name," is thirsty.")
			#Scavenging system driver.
			if person.scavenging == 1:
				if person.daysToScavengeFor == person.daysScavenging:
					# Now that they've finished scavenging, set everything to 0
					person.scavenging = 0
					person.daysToScavengeFor = 0
					person.daysScavenging = 0
				else:
					person.daysScavenging += 1
					#Randomly finds an item
					rand_item("player")
					health_loss=randint(0,50)
					person.HP-=health_loss
					if person.HP <= 0:
						person.die()
				if person.health<20:
					person.scavenging=0
					person.daysToScavengeFor = 0
					person.daysScavenging = 0
			
		auto_feed()		
		
		for room in all_rooms: #Performs daily room checks.
			room.update_production() #Updates production value for all rooms.
			if room.can_produce==1: #Causes rooms that can produce to produce
				self.produce()
	
		#Trader inventory updates with new items and loses some items.
		number=randint(0,len(trader_inventory)/5) #Loses a random number of items
		lose_items("trader",number) 
		number=randint(0,len(trader_inventory)/5) #Finds another random number.
		find_rand_item("trader",number) #Finds random number of items.
		
		#A raid should happen once every 5 days.
		raid_chance=randint(1,5)
		if day_count<11:
			raid_chance=1 #No raids should happen in the early days.
		if raid_chance>4:
			raid()
			
		if happiness<5:
				postition="lost"
		elif happiness<20:
			print("Warning. Your people are unhappy. You could lose your position if you don't improve the situation soon.")
		
				
		for r in rooms: #De-rushes every room that was rushed.
			if r.rushed==1:
				r.production-=50
				r.rushed=0
				
		while AP>0 and overuse==0: #Loops player actions.
			choice()
				
		happiness_loss()
		produce_all()
		update_defense()
		day_count+=1

			
	else: #Once game ends.
		if end==1:
			print("Too bad. You died.")
		elif postition=="lost":
			print("Too bad. You lost your postition because of your poor leadership skills.")
		again=input("Want to play again?")
		again=again[0].lower()
		if again=="y":
			game()
		else:
			print("Okay. Thanks for playing!!!")
game()