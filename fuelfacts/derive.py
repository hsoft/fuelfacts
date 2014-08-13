import yaml
from pint import UnitRegistry

from .util import unsource
from .eia import load_series

ureg = UnitRegistry()

def btu_to_liter(consts, btu):
    """Returns the number of liters of diesel required to give `btu`
    """
    diesel_bpg = consts['diesel']['btu-per-gallon'] * (ureg.btu / ureg.gallon)
    gallon = btu / diesel_bpg
    return gallon.to(ureg.l)

def compute_freight_consumption_per_liter(consts):
    diesel_kpl = consts['diesel']['kilogram-per-liter'] * (ureg.kg / ureg.l)
    freight = unsource(yaml.load(open('facts/freight.yaml', 'rb')))
    freight_bptm = {}
    for ftype, data in freight.items():
        freight_bptm[ftype] = data['btu-per-ton-mile'] * (ureg.btu / (ureg.ton * ureg.mile))
    freight_lplkm = {}
    for ftype, bptm in freight_bptm.items():
        # We have BTU per ton-mile. Let's go semi-metric
        bpkmkg = bptm.to(ureg.btu / (ureg.km * ureg.kg))
        # BTU per KM-KG, better. Now, let's apply diesel density to transform that into volume.
        bpkml = bpkmkg * diesel_kpl
        # Now, things get a bit weird because we have equivalent units on both side of our divider
        # and pint will automatically recude these. Since we already have our "kml" part figured
        # out, let's get rid of it.
        b = bpkml * (ureg.km * ureg.l)
        # Now, we have a number of BTU per km/L. Let's figure our how many liters of diesel are
        # needed to give us those BTUs
        l = btu_to_liter(consts, b)
        freight_lplkm[ftype] = {'liter-per-liter-km': {
            'value': l.magnitude,
            'source': 'derived',
        }}
    with open('derived/freight.yaml', 'wt') as fp:
        yaml.dump(freight_lplkm, fp)

def compute_refineries_consumption_per_liter(consts):
    natgas_bpcf = consts['natural-gas']['btu-per-cubic-foot'] * (ureg.btu / (ureg.foot ** 3))
    WANTED_EIA_SERIES = [
        'PET.MTTRX_NUS_1.A', # net US refineries production of everything, 1000s of barrels
        'PET.MGFRX_NUS_1.A', # net US refineries production of gasoline, 1000s of barrels
        'PET.8_NA_8FN0_NUS_2.A', # U.S. Natural Gas Consumed at Refineries, million cubic feet
        'PET.8_NA_8FE0_NUS_K.A', # U.S. Purchased Electricity Consumed at Refineries, million kwh
    ]
    eia_series = load_series('PET', WANTED_EIA_SERIES)
    prod_all, prod_gas, con_natgas, con_elec = [
        dict(serie['data'])['2013'] for serie in eia_series
    ]
    prod_all *= ureg.barrel * 1000
    prod_all_liter = prod_all.to(ureg.l)
    con_elec *= ureg.watt_hour * 1000
    con_elec_btu = con_elec.to(ureg.btu)
    #mcf = million cubic feet
    con_natgas *= (ureg.foot ** 3) * 1000000
    con_natgas_btu = con_natgas * natgas_bpcf
    tot_btu = con_natgas_btu + con_elec_btu
    con_btu_per_liter = tot_btu / prod_all_liter
    con_diesel_liter_per_liter = btu_to_liter(consts, con_btu_per_liter * ureg.l)
    refinery_lcplpi = {'gasoline': {'liter-consumed-per-liter-produced': {
        'value': con_diesel_liter_per_liter.magnitude,
        'source': 'derived',
    }}}
    with open('derived/refinery.yaml', 'wt') as fp:
        yaml.dump(refinery_lcplpi, fp)

def main():
    consts = unsource(yaml.load(open('facts/consts.yaml', 'rb')))
    compute_freight_consumption_per_liter(consts)
    compute_refineries_consumption_per_liter(consts)

if __name__ == '__main__':
    main()

