from random import randint, random
from sys import exit as sysexit
from typing import List

from rich import print

# from rich.table import Table
from rich.traceback import install

install(show_locals=True)

RAND_MAX = NotImplementedError

CITIES_LIST = [
    "Santa Paravia",
    "Fiumaccio",
    "Torricella",
    "Molinetto",
    "Fontanile",
    "Romanga",
    "Monterana",
]

MALE_TITLES = [
    "Sir",
    "Baron",
    "Count",
    "Marquis",
    "Duke",
    "Grand Duke",
    "Prince",
    "* H.R.H. King",
]

FEMALE_TITLES = [
    "Lady",
    "Baroness",
    "Countess",
    "Marquise",
    "Duchess",
    "Grand Duchess",
    "Princess",
    "* H.R.H. Queen",
]


class Player:
    def __init__(
        self, year: int, city: int, level: int, name: str, is_male: bool
    ) -> None:
        self.cathedral: int = 0
        self.city: str = CITIES_LIST[city]  # index-based
        self.clergy: int = 5
        self.customs_duty: int = 25
        self.customs_duty_revenue: int = 0  # not in original constructor
        self.difficutly: int = level
        self.dead_serfs: int = 0
        self.feeling_serfs: int = 0
        self.grain_price: int = 25
        self.grain_demand: int = 0  # not in original constructor
        self.grain_reserve: int = 5000
        self.harvest: int = 0
        self.income_tax: int = 5
        self.income_tax_revenue: int = 0  # not in original constructor
        self.invade_me: bool = False  # not in original constructor
        self.is_bankrupt: bool = False
        self.is_dead: bool = False
        self.i_won: bool = False
        self.justice: int = 2
        self.justice_revenue: int = 0  # not in original constructor
        self.land: int = 10000
        self.land_price: float = 10.0
        self.male_or_female: bool = is_male
        self.market_places: int = 0
        self.market_revenue: int = 0
        self.merchants: int = 25
        self.mill_revenue: int = 0
        self.mills: int = 0
        self.name: str = name
        self.new_serfs: int = 0
        self.nobles: int = 4
        self.old_title: int = 1
        self.palace = 0
        self.public_works: float = 1.0
        self.rats: int = 0
        self.rats_ate: int = 0
        self.sales_tax: int = 10
        self.sales_tax_revenue: int = 0  # not in original constructor
        self.serfs: int = 2000
        self.soldiers: int = 25
        self.soldier_pay: int = 0
        self.title_num = 1
        self.title = MALE_TITLES[0] if is_male else FEMALE_TITLES[0]
        if city == 6:
            self.title = "Baron"
        self.transplanted_serfs: int = 0
        self.treasury: int = 1000
        self.which_player: int = city
        self.year: int = year
        self.year_of_death: int = year + 20 + randint(0, 35)

        # char City[15], Name[25], Title[15];
        # float PublicWorks, LandPrice;
        # boolean InvadeMe, IsBankrupt, IsDead, IWon, MaleOrFemale, NewTitle;


def _print_instructions():
    print("Santa Paravia and Fiumaccio\n")
    print("You are the ruler of a 15th century Italian city state.")
    print("If you rule well, you will receive higher titles. The")
    print("first player to become king or queen wins. Life expectancy")
    print("then was brief, so you may not live long enough to win.")
    print("The computer will draw a map of your state. The size")
    print("of the area in the wall grows as you buy more land. The")
    print("size of the guard tower in the upper left corner shows")
    print("the adequacy of your defenses. If it shrinks, equip more")
    print("soldiers! If the horse and plowman is touching the top of the wall,")
    print("all your land is in production. Otherwise you need more")
    print("serfs, who will migrate to your state if you distribute")
    print("more grain than the minimum demand. If you distribute less")
    print("grain, some of your people will starve, and you will have")
    print("a high death rate. High taxes raise money, but slow down")
    print("economic growth. (Press ENTER to begin game)")
    input()


def generate_harvest(me: Player) -> None:
    # TODO: this should be a Player class method.
    me.harvest = (randint(0, 5) + randint(0, 6)) // 2
    me.rats = randint(0, 50)
    me.grain_reserve = ((me.grain_reserve * 100) - (me.grain_reserve * me.rats)) // 100


def new_land_and_grain_prices(me: Player) -> None:
    # TODO: this should be a Player class method.
    my_random: float = random()
    x: float = float(me.land)
    y = ((float(me.serfs) - float(me.mills)) * 100.0) * 5.0

    y = max(y, 0.0)
    if y < x:
        x = y
    y = me.grain_reserve * 2.0  # noqa: F841
    if y < x:
        x = y

    y = me.harvest + (my_random - 0.5)
    h: int = int(x * y)
    me.grain_reserve += h
    me.grain_demand = (
        me.nobles * 100
        + me.cathedral * 40
        + me.merchants * 30
        + me.soldiers * 10
        + me.serfs * 5
    )
    me.land_price = (3.0 * me.harvest + randint(0, 6) + 10.0) / 10.0
    if h < 0:
        h *= -1
    if h < 1:
        y = 2.0
    else:
        y = float(me.grain_demand) / float(h)
        y = min(y, 2.0)

    y = max(y, 0.8)

    me.land_price *= y

    me.land_price = max(me.land_price, 1.0)

    me.grain_price = int(
        (6.0 - me.harvest) * 3.0 + randint(0, 5) + randint(0, 5) * 4.0 * y
    )
    me.rats_ate = h


def print_grain(me: Player) -> None:
    # TODO: this does not have to access the player
    harvest = me.harvest
    if harvest == 1:
        print("Drought. Famine Threatens. ", end="")
    elif harvest == 2:
        print("Bad Weather. Poor Harvest. ", end="")
    elif harvest == 3:
        print("Normal Weather. Average Harvest. ", end="")
    elif harvest == 4:
        print("Good Weather. Fine Harvest. ", end="")
    elif harvest == 5:
        print("Excellent Weather. Great Harvest! ", end="")


def buy_grain(me: Player) -> None:
    # TODO: this should be a Player class method.
    a = input("How much grain do you want to buy (0 to specifiy a total)? ")
    how_much = int(a)

    if how_much == 0:
        a = input("How much total grain do you wish? ")
        how_much = int(a)
        how_much -= me.grain_reserve

        if how_much < 0:
            print("Invalid total amount.", end="\n\n")
            return

    me.treasury -= how_much * me.grain_price // 1000
    me.grain_reserve += how_much


def sell_grain(me: Player) -> None:
    # TODO: this should be a Player class method.

    a = input("How much grain do you want to sell? ")
    how_much = int(a)

    if how_much > me.grain_reserve:
        print("You don't have it.")
        return

    me.treasury += how_much * me.grain_price // 1000
    me.grain_reserve -= how_much


def buy_land(me: Player) -> None:
    # TODO: this should be a Player class method.

    a = input("How much land do you want to buy? ")
    how_much = int(a)

    me.land += how_much
    me.treasury -= int(how_much * me.land_price)


def sell_land(me: Player) -> None:
    # TODO: this should be a Player class method.

    a = input("How much land do you want to sell? ")
    how_much = int(a)
    if how_much > me.land - 5000:
        print("You can't sell that much.")
        return
    me.land -= how_much
    me.treasury += int(how_much * me.land_price)


def buy_sell_grain(me: Player) -> None:
    # TODO: this should be a Player class method.
    finished: bool = False

    while finished is False:  # line 943
        print(f"\nYear {me.year}")
        print(f"\n{me.title} {me.name}")
        print(f"Rats ate {me.rats}% of your grain resources.")
        print_grain(me)
        print(f"({me.rats_ate} steres)")
        # TODO: use tabulation libraries
        print("Grain\tGrain\tPrice of\tPrice of\tTreasury")
        print("Reserve\tDemand\tGrain\t\tLand")
        print(
            f"{me.grain_reserve}\t{me.grain_demand}\t{me.grain_price}\t\t{me.land_price:.2f}\t\t{me.treasury}"  # noqa: E501
        )
        print("steres\tsteres\t1000 st.\thectare\t\tgold florins")
        print(f"\nYou have {me.land} hectares of land.")
        print("\n1. Buy grain, 2. Sell grain, 3. Buy land, 4. Sell land")
        usr_input = input("(Enter q to continue): ")

        if usr_input[0] == "q":
            finished = True
        elif usr_input[0] == "1":
            buy_grain(me)
        elif usr_input[0] == "2":
            sell_grain(me)
        elif usr_input[0] == "3":
            buy_land(me)
        elif usr_input[0] == "4":
            sell_land(me)


def serfs_procreating(me: Player, my_scale: float) -> None:

    absc = int(my_scale)
    ord = my_scale - absc
    # FIXME: this could be randint(ord, ord+absc)
    # TODO: does it really have to be part of the player object?
    me.new_serfs = int((randint(0, absc) + ord) * me.serfs / 100.0)
    me.serfs += me.new_serfs
    print(f"{me.new_serfs} serfs born this year.")


def serfs_decomposing(me: Player, my_scale: float) -> None:
    absc = int(my_scale)
    ord = my_scale - absc
    # FIXME: this could be randint(ord, ord+absc)
    # TODO: does it really have to be part of the player object?
    me.dead_serfs = int((randint(0, absc) + ord) * me.serfs / 100.0)
    me.serfs -= me.dead_serfs
    print(f"{me.dead_serfs} die this year.")


def release_grain(me: Player) -> int:

    is_ok: bool = False
    minimum = me.grain_reserve // 5
    maximum = me.grain_reserve - minimum

    while is_ok is False:
        print("How much grain will you release for consumption?")
        how_much = int(
            input(f"1 = Minimum ({minimum}), 2 = Maximum({maximum}), or enter a value:")
        )
        if how_much == 1:
            how_much = minimum
        if how_much == 2:
            how_much = maximum

        # Are we being a Scrooge?
        if how_much < minimum:
            print("You must release at least 20% of your reserves.")
        elif how_much > maximum:
            print("You must keep at least 20%.")
        else:
            is_ok = True

    me.soldier_pay = 0
    me.market_revenue = 0
    me.new_serfs = 0
    me.dead_serfs = 0
    me.transplanted_serfs = 0
    me.feeling_serfs = 9
    me.invade_me = False
    me.grain_reserve -= how_much

    z: float = how_much / me.grain_demand - 1.0

    if z > 0.0:
        z /= 2.0
    if z > 0.25:
        z = z / 10.0 + 0.25

    zp: float = 50.0 - me.customs_duty - me.sales_tax - me.income_tax
    if zp < 0.0:
        zp *= me.justice
    zp /= 10.0
    if zp > 0.0:
        zp += 3.0 - me.justice
    z += zp / 10.0
    z = min(z, 0.5)

    # line 652
    if how_much < me.grain_demand - 1:
        x = (me.grain_demand - how_much) / me.grain_demand * 100.0 - 9.0
        xp = x
        x = min(x, 65.0)
        if x < 0.0:
            xp = 0.0
            x = 0.0
        serfs_procreating(me, 3.0)
        serfs_decomposing(me, xp + 8.0)
    else:
        serfs_procreating(me, 7.0)
        serfs_decomposing(me, 3.0)

        if (me.customs_duty + me.sales_tax) < 35:
            me.merchants += randint(0, 4)
        if me.income_tax < randint(0, 28):
            me.nobles += randint(0, 2)
            me.clergy += randint(0, 3)

        if how_much > me.grain_demand * 1.3:
            zp = me.serfs / 1000.0
            z = (how_much - me.grain_demand) / me.grain_demand * 10.0
            z *= zp * randint(0, 25)
            z += 40 * random()
            # TODO: shall transplanted serfs be part of the player object?
            me.transplanted_serfs = int(z)  # :691
            me.serfs += me.transplanted_serfs
            print(f"{me.transplanted_serfs} serfs move to the city")
            z = zp * random() / RAND_MAX

            z = min(z, 50.0)

            me.merchants += int(z)
            me.nobles += 1
            me.clergy += 2

    if me.justice > 2:  # line 706
        me.justice_revenue = int(me.serfs / 100 * (me.justice - 2) * (me.justice - 2))
        me.justice_revenue = randint(0, me.justice_revenue)
        me.serfs -= me.justice_revenue
        me.feeling_serfs = me.justice_revenue
        print(f"{me.feeling_serfs} serfs harsh justice")

    me.market_revenue = me.market_places * 75

    if me.market_revenue > 0:
        me.treasury += me.market_revenue
        print(f"Your market earned {me.market_revenue} florins.")

    # FIXME: why not using randint(55, 305)?
    me.mill_revenue = me.mills * (55 + randint(0, 250))

    if me.mill_revenue > 0:
        me.treasury += me.mill_revenue
        print(f"Your woolen mill earned {me.mill_revenue} florins.")

    me.soldier_pay = me.soldiers * 3
    me.treasury -= me.soldier_pay
    print(f"You paid your soldiers {me.soldier_pay} florins.")
    print(f"You have {me.serfs} serfs in your city.")
    input("(Press ENTER): ")

    if me.land // 1000 > me.soldiers:
        me.invade_me = True
        return 3

    if me.land // 500 > me.soldiers:
        me.invade_me = True
        return 3

    return 0


def attack_neighbour(me: Player, him: Player) -> int:
    if me.which_player == 7:
        land_taken: int = randint(1000, 10000)
    else:
        land_taken = me.soldiers * 1000 - (me.land // 3)

    if land_taken > (him.land - 5000):
        land_taken = (him.land - 5000) // 2

    me.land += land_taken
    him.land -= land_taken

    print(
        f"\a\n{me.title} {me.name} of {me.city} invades and seizes {land_taken} hectares of land!"  # noqa E501
    )

    dead_soldiers: int = randint(0, 40)
    dead_soldiers = min(dead_soldiers, him.soldiers - 15)
    him.soldiers -= dead_soldiers
    print(f"{him.title} {him.name} loses {dead_soldiers} soldiers in battle.")
    return land_taken


def generate_income(me: Player) -> None:
    # TODO: this should be a Player class method.
    me.justice_revenue = (me.justice * 300 - 500) * me.title_num

    if me.justice == 1:
        string = "Very Fair"
    elif me.justice == 2:
        string = "Moderate"
    elif me.justice == 3:
        string = "Harsh"
    elif me.justice == 4:
        string = "Outrageous"

    y: float = 150.0 - me.sales_tax - me.customs_duty - me.income_tax
    y = max(y, 1.0)
    y /= 100.0
    # in the original code (:466) you fiddle with the object's parameters
    # this leads to mypy complaining as it changes from int to float then to int
    customs_duty_revenue: float = (
        me.nobles * 180
        + me.clergy * 75
        + me.merchants * 20 * y
        + me.public_works * 100.0
    )
    me.customs_duty_revenue = int(me.customs_duty / 100.0 * customs_duty_revenue)

    me.sales_tax_revenue = int(
        (me.nobles * 50 + me.merchants * 25 + int(me.public_works * 10))
        * y
        * (5 - me.justice)
        * me.sales_tax
        / 200
    )

    me.income_tax_revenue = int(
        (me.nobles * 250 + me.public_works * 20.0 + 10 * me.justice * me.nobles * y)
        * me.income_tax
        / 100
    )

    revenues: int = (
        me.customs_duty_revenue
        + me.sales_tax_revenue
        + me.income_tax_revenue
        + me.justice_revenue
    )
    print(f"State revenues {revenues} gold florins.")
    # TODO: use tabulation libraries
    print("Customes Duty\tSales Tax\tIncome Tax\tJustice")
    print(
        f"{me.customs_duty_revenue}\t{me.sales_tax_revenue}\t{me.income_tax_revenue}\t{string}"  # noqa:E501
    )


def add_revenue(me: Player) -> None:
    # TODO: this should be a Player class method.
    me.treasury += (
        me.justice_revenue
        + me.customs_duty_revenue
        + me.income_tax_revenue
        + me.sales_tax_revenue
    )
    # Penalise deficit spending.
    if me.treasury < 0:
        me.treasury = int(me.treasury * 1.5)
    # Will a title make the crediors happy (for now)?
    if me.treasury < -10000 * me.title_num:
        me.is_bankrupt = True


def seize_assets(me: Player) -> None:
    # TODO: this should be a Player class method.
    me.market_places = 0
    me.palace = 0
    me.cathedral = 0
    me.mills = 0
    me.land = 6000
    me.treasury = 100
    me.is_bankrupt = False
    print(f"\n\n{me.title} {me.name} is bankrupt.")
    print("\nCreditors have seized much of your assets.")
    input("\n(Press ENTER): ")


def adjust_tax(me: Player) -> None:
    # TODO: this should be a Player class method.
    val: int = 1
    duty: int = 0
    usr_in = "\0"

    while val != 0 or usr_in[0] != "q":
        print(f"\n{me.title} {me.name}\n")
        generate_income(me)
        # TODO: use tabulation libraries
        print(f"({me.customs_duty})\t\t({me.sales_tax})\t\t({me.income_tax})")
        print()
        print("1. Customs Duty, 2. Sales Tax, 3. Wealth Tax, 4. Justice")
        usr_in = input("Enter tax number for changes, q to continue: ")

        if "q" not in usr_in:
            val = int(usr_in)

            if val == 1:
                duty = int(input("New customs duty (0 to 100): "))
                duty = min(duty, 100)
                duty = max(duty, 0)
                me.customs_duty = duty
            elif val == 2:
                duty = int(input("New sales tax (0 to 50): "))
                duty = min(duty, 50)
                duty = max(duty, 0)
                me.sales_tax = duty
            elif val == 3:
                duty = int(input("New wealth tax (0 to 25): "))
                duty = min(duty, 25)
                duty = max(duty, 0)
                me.income_tax = duty
            elif val == 4:
                duty = int(
                    input(
                        "Justice: 1. Very fair, 2. Moderate, 3. Harsh, 4. Outrageous: "
                    )
                )
                duty = min(duty, 4)
                duty = max(duty, 1)
                me.justice = duty

    add_revenue(me)

    if me.is_bankrupt:
        seize_assets(me)


def draw_map(me: Player):
    # Not implemented yet.
    pass


def buy_market(me: Player) -> None:
    # TODO: this should be a Player class method.
    me.market_places += 1
    me.merchants += 5
    me.treasury -= 1000
    me.public_works += 1.0


def buy_mill(me: Player) -> None:
    # TODO: this should be a Player class method.
    me.mills += 1
    me.treasury -= 2000
    me.public_works += 0.25


def buy_cathedral(me: Player) -> None:
    # TODO: this should be a Player class method.
    me.cathedral += 1
    me.clergy += randint(0, 6)
    me.treasury -= 5000
    me.public_works += 1.0


def buy_soldiers(me: Player) -> None:
    # TODO: this should be a Player class method.
    me.soldiers += 20
    me.serfs -= 20
    me.treasury -= 500


def buy_palace(me: Player) -> None:
    # TODO: this should be a Player class method.
    me.palace += 1
    me.nobles += randint(0, 2)
    me.treasury -= 3000
    me.public_works += 0.5


def show_stats(my_players: List[Player], how_many: int) -> None:
    # FIXME: use table tools such as tabulate or rich
    print("Nobles\tSoldiers\tClergy\tMerchants\tSerfs\tLand\tTreasury")
    for my_player in my_players:
        print(
            "\n%s %s\n%d\t%d\t\t%d\t%d\t\t%d\t%d\t%d\n",
            my_player.title,
            my_player.name,
            my_player.nobles,
            my_player.soldiers,
            my_player.clergy,
            my_player.merchants,
            my_player.serfs,
            my_player.land,
            my_player.treasury,
        )

    input("\n(Press ENTER): ")


def state_purchases(me: Player, how_many: int, my_players: List[Player]) -> None:
    val: int = 1
    read_input: str = "\0"

    while val != 0 or read_input[0] not in ("q"):
        print("\n\n")
        print(f"{me.title} {me.name}\nState purchases.")
        print()  # extra line
        print(f"1. Marketplace ({me.market_places})\t\t\t\t1000 florins")
        print(f"2. Woolen mill ({me.mills})\t\t\t\t2000 florins")
        print(f"3. Palace (partial) ({me.palace})\t\t\t\t3000 florins")
        print(f"4. Cathedral (partial) ({me.cathedral})\t\t\t5000 florins")
        print("5. Equip one platoon of serfs as soldiers\t500 florins")
        print(f"\nYou have {me.treasury} gold florins.")
        print("\nTo continue, enter q. To compare standings, enter 6")

        val = int(input("Your choice: "))
        if val == 1:
            buy_market(me)
        elif val == 2:
            buy_mill(me)
        elif val == 3:
            buy_palace(me)
        elif val == 4:
            buy_cathedral(me)
        elif val == 5:
            buy_soldiers(me)
        elif val == 6:
            show_stats(my_players, how_many)

    return


def __limit10(num: int, denom: int) -> int:
    val = num // denom
    return max(val, 10)


def __change_title(me: Player) -> None:
    # TODO: this should be a Player class method.
    if me.male_or_female:
        me.title = MALE_TITLES[me.title_num]
    else:
        me.title = FEMALE_TITLES[me.title_num]

    if me.title_num == 7:
        me.i_won = True
        return

    return


def check_new_title(me: Player) -> bool:
    # TODO: this should be a Player class method.
    total: int = 0
    total += __limit10(me.market_places, 1)
    total += __limit10(me.palace, 1)
    total += __limit10(me.cathedral, 1)
    total += __limit10(me.mills, 1)
    total += __limit10(me.treasury, 5000)
    total += __limit10(me.land, 6000)
    total += __limit10(me.merchants, 50)
    total += __limit10(me.nobles, 5)
    total += __limit10(me.soldiers, 50)
    total += __limit10(me.clergy, 10)
    total += __limit10(me.serfs, 2000)
    total += __limit10(int(me.public_works * 100.0), 500)
    me.title_num = total // me.difficutly - me.justice
    me.title_num = min(me.title_num, 7)
    me.title_num = max(me.title_num, 0)

    # did we change (could be backwards of forwards)?
    if me.title_num > me.old_title:
        me.old_title = me.title_num
        __change_title(me)
        print(f"\aGood news! {me.name} had achieved the rank of {me.title}", end="\n\n")
        return True

    me.title_num = me.old_title
    return False


def im_dead(me: Player) -> None:
    # TODO: this should be a Player class method.
    print("\n\nVery sad news.")
    print(f"{me.title} {me.name} has just died.")
    if me.year > 1450:
        print("of old age after a long reign.")
    else:
        why: int = randint(0, 8)
        if why == 3:
            print("of pneumonia afer a cold winter in a drafty castle.")
        elif why == 4:
            print("of typhoid after drinking contaminated water.")
        elif why == 5:
            print("in a smallpox epidemic.")
        elif why == 6:
            print("after being attacked by robbers while travelling.")
        elif why == 8:
            print("of food poisoning")

    me.is_dead = True
    input("(Press ENTER): ")


def new_turn(
    me: Player, how_many: int, my_players: List[Player], baron: Player
) -> None:

    generate_harvest(me)
    new_land_and_grain_prices(me)
    buy_sell_grain(me)
    release_grain(me)

    if me.invade_me:
        for idx in range(how_many):
            if idx != me.which_player and my_players[idx].soldiers > me.soldiers * 2.4:
                attack_neighbour(my_players[idx], me)
                break
        else:
            attack_neighbour(baron, me)

    adjust_tax(me)
    draw_map(me)
    state_purchases(me, how_many, my_players)
    check_new_title(me)

    me.year += 1
    if me.year == me.year_of_death:
        im_dead(me)

    if me.title_num >= 7:
        me.i_won = True


def play_game(my_players: List[Player], num_of_players: int) -> None:
    all_dead: bool = False
    winner: bool = False
    # winning_player: Optional[Player] = None
    baron = Player(1400, 6, 4, "Peppone", True)

    while not all_dead and not winner:
        for my_player in my_players:
            if not my_player.is_dead:
                new_turn(my_player, num_of_players, my_players, baron)
        all_dead = not any(
            all_dead and my_player.is_dead is False for my_player in my_players
        )
        for my_player in my_players:
            if my_player.i_won:
                winner = True
                winning_player: Player = my_player
                break

    if all_dead:
        print("The game has ended.")
        return

    print(f"Game Over. {winning_player.title} {winning_player.name} wins.")
    return


def main() -> None:
    print("Santa Paravia and Fiumaccio")

    # FIXME: index out of range when simply pressed enter
    # instructions
    show_instr = input("Do you wish instrunctionsn (Y or N)? ")
    if show_instr[0] in ["y", "Y"]:
        _print_instructions()

    # number of players
    num_of_players = int(input("How many people want to play (1 to 6)? "))
    if num_of_players < 1 or num_of_players > 6:
        print("Thanks for playing.")
        sysexit()

    # difficulty level
    print(
        """What will be the difficulty of this game:
1. Apprentice
2. Journeyman
3. Master
4. Grand Master"""
    )

    level = int(input("Choose: "))
    level = max(level, 1)
    level = min(level, 4)

    my_players: List[Player] = []
    for idx in range(num_of_players):
        name = input(f"Who is the ruler of {CITIES_LIST[idx]}? ").strip()
        gender = input(f"Is {name} a man or a woman? (M or F)? ")
        m_or_f = gender[0] in ("m", "M")
        my_players.append(Player(1400, idx, level, name, m_or_f))

    # enter the main game loop
    play_game(my_players, num_of_players)


if __name__ == "__main__":
    main()
