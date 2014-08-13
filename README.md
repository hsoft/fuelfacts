# FuelFacts

*For every liter of fuel you consume, how much energy was needed to bring that fuel from oil fields
to your car?*

That's the question we try to answer with this application. The computation is complex, dependant
on many factors and needs data from many sources.

* Where does the oil come from?
* What kind of crude was it?
* How was it shipped?
* Where was it refined?
* How many oil spills lately? Middle east pipeline sabotage?

Because of the overwhelming complexity of the task, the approach taken here is to have gross
approximations that will be refined (pun intended) over time with additional knowledge about the
process and access to more precise data.

However approximate the computations are, the driving principle behind this app is to keep them
clear by:

* Having a source for every constant fact.
* Having an explanation page for each calculation.

# Installation

All you need is Python 3.4. Then, you can do this:

    $ pyvenv env
    $ . env/bin/activate
    $ pip install requirements.txt
    $ python -m fuelfacts.derive
    $ python run.py

Then, you can open the indicated URL in your browser to use the application.

Note that Python 3.3 should work, but you'll have to install pip manually in your virtualenv.

# Deriving facts

The `python -m fuelfacts.derive` part computes ready-to-use facts from "constant" facts, that is,
facts taken directly from a trusted source.

Often, facts are given in units that aren't readily usable. For example, we'll know how many BTU
per ton-mile a freight ship typically consumes, but the problem is that we want units in the metric
system and we want consumption info for volume, not weight. By mixing this fact with gasoline
density (another constant fact), and doing some unit conversions (those end up really hurting my
head), we can derive a freight ship typical consumpption per liter of gasoline transported over a
kilometer. Voila!

