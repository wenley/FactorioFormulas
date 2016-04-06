
# Factorio Formulas

A small utility to recall recipes for items and also give the building set, raw materials, and time to craft a certain number of items.

## Terminology

* **Item** = A thing that can occupy an inventory slot or be consumed. Examples: Iron Gears, Copper Coil, Sulfuric Acid.
* **Recipe** = The immediate inputs, time, and output amount when making an item.
* **Tick** = A unit of time equal to 0.5 seconds. Created for convenience since many early game recipes only take 0.5 seconds.
* **Building** = Catch-all term for all production facilities. Includes assembly machines, chemical plants, and offshore pumps.

Note that I abbreviate many items' names relative to the in-game name. For example, `Copper Cable` becomes `coil`, `Electronic Circuit` becomes `circuit`, and `Red Science Pack` becomes `science_1`. Hopefully all the names are still immediately obvious, but I apologize in advance for any confusion.

## Usage

Taken from the help description:
```
Usage: factorio.py [options]

Options:
  -h, --help            show this help message and exit
  -r RECIPE_REQUESTED, --recipe=RECIPE_REQUESTED
                        Item whose recipe to recite.
  -b BUILD_TARGET, --build=BUILD_TARGET
                        Item to determine build for.
  -a AMOUNT, --amount=AMOUNT
                        Amount of the item being built. [default 1].
  -t TICKS, --time=TICKS
                        Number of ticks allowed per batch. Defaults to the
                        recipe time.
  -v, --verbose         Turn on logging.
```

### Examples

```
$ python factorio.py -l

...
```

```
$ python factorio.py -r inserter
1 inserter = 1 iron, 1 circuit, 1 gear + 1 ticks across 1 buildings
```

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
