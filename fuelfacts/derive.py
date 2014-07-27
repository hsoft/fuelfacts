import yaml
from pint import UnitRegistry
ureg = UnitRegistry()

def main():
    diesel = yaml.load(open('facts/diesel.yaml', 'rb'))
    diesel_bpg = diesel['btu-per-gallon']['value'] * (ureg.btu / ureg.gallon)
    diesel_kpl = diesel['kilogram-per-liter']['value'] * (ureg.kg / ureg.l)
    freight = yaml.load(open('facts/freight.yaml', 'rb'))
    freight_bptm = {}
    for ftype, data in freight.items():
        freight_bptm[ftype] = data['btu-per-ton-mile']['value'] * (ureg.btu / (ureg.ton * ureg.mile))
    freight_lplkm = {}
    for ftype, bptm in freight_bptm.items():
        print(ftype)
        # We have BTU per ton-mile. Let's go semi-metric
        print(bptm)
        bpkmkg = bptm.to(ureg.btu / (ureg.km * ureg.kg))
        # BTU per KM-KG, better. Now, let's apply diesel density to transform that into volume.
        print(bpkmkg)
        bpkml = bpkmkg * diesel_kpl
        # Now, things get a bit weird because we have equivalent units on both side of our divider
        # and pint will automatically recude these. Since we already have our "kml" part figured
        # out, let's get rid of it.
        b = bpkml * (ureg.km * ureg.l)
        # Now, we have a number of BTU per km/L. Let's figure our how many gallons of diesel are
        # needed to give us those BTUs
        print(b)
        g = b / diesel_bpg
        print(g)
        # good! now, let's go full-metric.
        l = g.to(ureg.l)
        print('{:0.6f}'.format(l))
        freight_lplkm[ftype] = {'liter-per-liter-km': {
            'value': l.magnitude,
            'source': 'derived',
        }}
    with open('derived/freight.yaml', 'wt') as fp:
        yaml.dump(freight_lplkm, fp)

if __name__ == '__main__':
    main()

