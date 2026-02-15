world = {
    "Cryo Chamber":{
        "description":"A cold, sterile room filled with frosted glass tubes. The cryo pod you woke up in still hisses with escaping vapor. Emergency lights flicker red along the ceiling.",
        "exits": {
            "west":"Main Corridor"
        },
        "items": [],
    },
    "Main Corridor":{
        "description" :"A long metallic hallway stretching through the ship's center. Panels flicker with partial power, and distant thuds echo through the hull. The atmosphere feels unstable.",
        "exits":{
            "north":"Engineering Bay",
            "west":"Armory",
            "east":"Cryo Chamber",
            "south":"Bridge",
        },
        "items":[]
    },
    "Engineering Bay":{
        "description":"Sparks pop from exposed wires, and a half-functional console flashes warnings. Tools float slightly as if gravity is unstable here. Something important was left behind.",
        "exits":{
            "south":"Main Corridor"
        },
        "items":["keycard"],
    },
    "Armory":{
        "description":"Racks of weapons and equipment line the walls, though most slots are empty. A few emergency lights cast harsh shadows across the scattered crates.",
        "exits":{
            "east":"Main Corridor"
        },
        "items":["pulse rifle"]
    },
    "Bridge":{
        "description":"The ship's main control room, lined with glowing consoles and centered around a large viewport overlooking the stars.",
        "exits":{
            "north":"Main Corridor",
            "south":"Escape Pod Bay"
        },
        "items":["burger"],
        "locked":True
    },
    "Escape Pod Bay":{
        "description":"Rows of compact escape pods rest in their docks, one of them powered and waiting. A clear viewport shows the stars drifting outside the ship.",
        "exits":{
            "north":"Bridge",
            "east":"Escape Pod"
        },
        "items":[],
        "enemy":"alien"
    },
    "Escape Pod":{
        "exits":{
            "west":"Escape Pod Bay"
        },
        "items":[]

    },
    "items":{
        "keycard":{
            "description":"A plastic keycard with the word Bridge written on it."
        },
        "pulse rifle":{
            "description":"A heavy weapon that shoots strong pulses of energy, disintegrating anything in its path."
        },
        "burger":{
            "description":"A Big-Mac from McDonalds."
        }
    }
}

current_room = "Cryo Chamber"
inventory = []
playing = True

print("\nYour eyes snap open to the hiss of escaping vapor. Frost clings to the walls of the cryo chamber, and somewhere deep in the ship, an alarm wails—you're not alone, and you have no time to waste.\n"
"\nExplore the ship and return home using the Escape Pod.")
print("\n<type help for command list>\n")
while playing:
    
    print("__"f"{current_room}""__")
    

    command = input(">").lower().strip()
    words = command.split()

    if len(words) == 0:
        continue

    action = words[0]

    if action == "inventory":
        print(f"__INVENTORY__")
        for item in inventory:
            print(" -",item)
    
    # Take action
    elif action == "take":
        if len(words) < 2:
            print("Take what?")
            continue
        item = " ".join(words[1:])

        if item in world[current_room]["items"]:
            world[current_room]["items"].remove(item)
            inventory.append(item)
            print(f"You've aquired the {item}!")
        else:
            print("That item isn't here.")
        continue


    # Look action
    elif action == "look":
        print(world[current_room]["description"])
        
        if world[current_room]["items"]:
            print("Items here:", ", ".join(world[current_room]["items"]))
    
        print("Exits:", ", ".join(world[current_room]["exits"].keys()))
        continue

    elif action == "inspect":
        if len(words) < 2:
            print("Inspect what?")
            continue

        item = " ".join(words[1:])

        if item in inventory:
            print(world["items"][item]["description"])
        else:
            print("You don't have that item.")
        continue
    
    # Help action
    elif action == "help":
        print("Commands:")
        print("  take <item>")
        print("  inventory")
        print("  inspect <item>")
        print("  look")
        print("  go <direction>")
        print("  use <item>")
        continue
    
    # Go action
    elif action == "go":
        if len(words) < 2:
            print("Go where?")
            continue

        direction = words[1]

        if direction not in world[current_room]["exits"]:
            print("You can't go that way.")
            continue

        next_room = world[current_room]["exits"][direction]

        if "locked" in world[next_room] and world[next_room]["locked"]:
            print("The reinforced door slides only a few inches before stopping. A scanner beside it glows faintly, waiting for authorized access.")
            print(f"The {next_room} door is locked. You need a keycard.")
            continue
                
        if next_room == "Escape Pod":
            if "enemy" in world["Escape Pod Bay"]:
                print("The alien attacks as you try to leave, suffering the same fate as your crew members.")
                restart = input("Do you want to try again from the Cryo Chamber? (yes/no): ").lower().strip()

                if restart == "yes":
                    current_room = "Cryo Chamber"
                    inventory.clear()
                    print("---GAME RESTARTED---")
                    print("Your eyes snap open to the hiss of escaping vapor. Frost clings to the walls of the cryo chamber, and somewhere deep in the ship, an alarm wails—you're not alone, and you have no time to waste.")
                else:
                    print("+GAME OVER+")
                    playing = False
                continue

            else:
                print("| Ending #1 |")
                print("You finally step into the escape pod. As the hatch closes behind you, the stars stretch out ahead, your course set for home among the endless void.")
                print("You've successfuly escaped!")
                print("+GAME OVER+")
                playing = False
                continue

        current_room = next_room
        print(f"You move {direction} into the {current_room}.")

        if current_room == "Escape Pod Bay":
            if "enemy" in world["Escape Pod Bay"]:
                if ("pulse rifle" not in inventory) and ("burger" not in inventory):
                    print("There is an alien in the way, find a pulse rifle to exterminate it or perhaps another way.")
                    continue
                else:
                    print("The alien is blocking the Escape Pod. What will you do?")
   
    # Use action
    elif action == "use":
        if len(words) < 2:
            print("Use what?")
            continue

        item = " ".join(words[1:])

        if item == "keycard":
            
            if "keycard" not in inventory:
                print("You don't have the keycard.")
                continue

            elif current_room == "Main Corridor":
                if world["Bridge"]["locked"]:
                    world["Bridge"]["locked"] = False
                    print("You swipe the keycard... The Bridge door unlocks!")
                else:
                    print("The Bridge door is already unlocked.")

            elif current_room == "Bridge":
                print("You're already inside the Bridge. The door is behind you and unlocked.")

            else:
                print("You can't use the keycard here.")
    
        elif item == "pulse rifle":
            if "pulse rifle" not in inventory:
                print("You don't have the pulse rifle.")

            elif current_room == "Escape Pod Bay": 
                if "enemy" in world["Escape Pod Bay"]:
                    del world["Escape Pod Bay"]["enemy"]
                    print("Your shot punches through it and the alien falls silent.")
                    print("The Escape Pod is to the east.")

        elif item == "burger":
            if "burger" not in inventory:
                print("You don't have the burger.")
            
            elif current_room == "Escape Pod Bay":
                if "enemy" in world["Escape Pod Bay"]:
                    inventory.remove("burger")
                    print("You give the burger to the alien as a peace offering. The alien takes it, and you befriend the creature.")
                    
                    choice = input("Do you want to leave the ship togther? (yes/no): ")
                    if choice == "yes":
                        del world["Escape Pod Bay"]["enemy"]
                        print("| Ending #2 |")
                        print("You and the alien get into the Escape Pod and drift away from the ship as friends, looking for a new place to call home.")
                        print("+GAME OVER+")
                        playing = False
        continue
                

    else:
        print("I don't understand that command (type help for list).")
        continue