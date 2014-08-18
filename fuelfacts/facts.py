import yaml

from .util import unsource

supply = yaml.load(open('facts/supply.yaml', 'rb'))
consts = unsource(yaml.load(open('facts/consts.yaml', 'rb')))
freight = unsource(yaml.load(open('derived/freight.yaml', 'rb')))
refinery = unsource(yaml.load(open('derived/refinery.yaml', 'rb')))
calculation = yaml.load(open('derived/calculation.yaml', 'rb'))

