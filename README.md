
# Factorio Formulas

A small utility to recall recipes for items and also give the building set, raw materials, and time to craft a certain number of items.

## Disclaimer

I originally built this to be useful to me and it certainly shows.
`recipes.yaml` is woefully incomplete
(especially compared to [this amazing spreadsheet](https://docs.google.com/spreadsheets/d/1GKzEAf2IOGB5D2TCdX3tgisJmD1yikzQRJ31_Rxz7FM/edit#gid=0)),
but includes the recipes I've used and planned with most often.
The tags in it are also based on my mental organization of the different items.

I whole-heartedly welcome pull-requests, and please use the `recipes.yaml`. I hope it proves reusable in other analyses and tools.

## Terminology

* **Item** = A thing that can occupy an inventory slot or be consumed. Examples: Iron Gears, Copper Coil, Sulfuric Acid.
* **Recipe** = The immediate inputs, time, and output amount when making an item.
* **Tick** = A unit of time equal to 0.5 seconds. Created for convenience since many early game recipes only take 0.5 seconds.
* **Building** = Catch-all term for all production facilities. Includes assembly machines, chemical plants, and offshore pumps.

Note that I abbreviate many items' names relative to the in-game name.
For example, `Copper Cable` becomes `cable`, `Electronic Circuit` becomes `circuit`, and `Red Science Pack` becomes `science_1`.
Hopefully all the names are still immediately clear.

## Usage

Taken from the help description:
```
Usage: factorio.py [options]

Options:
  -h, --help            show this help message and exit
  -l, --list            Print a list of recipes.
  -v, --verbose         Turn on listing tags.
  --tag=TAGS            Only print recipes with the specified tag. Can be
                        listed multiple times.
  -r RECIPE_REQUESTED, --recipe=RECIPE_REQUESTED
                        Item whose recipe to recite.
  -b BUILD_TARGET, --build=BUILD_TARGET
                        Item to determine build for.
  -a AMOUNT, --amount=AMOUNT
                        Amount of the item being built. [default 1].
  -t TICKS, --ticks=TICKS
                        Number of ticks allowed per batch. 1 tick = 0.5 sec.
                        Defaults to the recipe time.
```

### Examples

#### Listing recipe names

Basic
```
$ python factorio.py -l
gear
coil
pipe
steel
...
```

With associated tags (determined by me):
```
$ python factorio.py -l -v
gear [intermediate]
coil [intermediate]
pipe
steel [intermediate]
circuit [intermediate,electronic]
```

Drilling down into a specific tag:
```
$ python factorio.py -l --tag combat -v
gun_turret
regular_magazine
piercing_magazine
regular_shells
piercing_shells
laser_turret [electronic]
```


#### Explain a recipe

```
$ python factorio.py -r inserter
1 inserter = 1 iron, 1 circuit, 1 gear + 1 ticks across 1 buildings
```

#### Printing a full build

Basic
```
$ python factorio.py -b inserter
For 1 inserter in 1 ticks:
Machines:
2 (1.50) coil
1 inserter
1 gear
1 circuit
Raws:
2 (1.50) copper
4 iron
```

Specifying an amount
```
$ python factorio.py -b inserter -a 4
For 4 inserter in 1 ticks:
Machines:
6 coil
4 inserter
4 gear
4 circuit
Raws:
6 copper
16 iron
```

Specifying an amount and specific number of ticks:
```
$ python factorio.py -b inserter -a 4 -t 2
For 4 inserter in 2 ticks:
Machines:
3 coil
2 inserter
2 gear
2 circuit
Raws:
6 copper
16 iron
```

## TODO

* Fill out `recipes.yaml` to be complete
* Account for different build rates of assemblers
* Account for using different modules in buildings (?)
* D3 Graph to show flow of items through buildings listed in a build
  - Allow splitting a block of buildings (circuits) into two nodes for building organization
