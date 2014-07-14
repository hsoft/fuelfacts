import yaml
from units import unit
from units.predefined import define_units

def main():
    define_units()
    LITER = unit('L')
    KILOGRAM = unit('kg')
    TON = unit('ton')
    MILE = unit('mi')
    KM = unit('km')
    TONMILE = TON * MILE
    GALLON = unit('gal')
    KILOGRAM_PER_LITER = KILOGRAM / LITER
    GPTM = GALLON / (TON * MILE)
    print(TON(1) * MILE(2))
    transport = yaml.load(open('facts/transport.yaml', 'rb'))
    print(repr(transport))
    weight = yaml.load(open('facts/weight.yaml', 'rb'))
    print(repr(weight))
    gasoline_density = KILOGRAM_PER_LITER(weight['gasoline']['density']['kilogram-per-liter']['value'])
    print(gasoline_density)
    truck_gptm = GPTM(transport['truck']['mileage']['gallons-per-thousand-ton-miles']['value'] / 1000)
    print(truck_gptm)
    tonmile = TONMILE(TON(gasoline_density * LITER(1)) * MILE(KM(1)))
    print(tonmile)
    liter_per_liter_km = LITER(tonmile * truck_gptm).num
    print(liter_per_liter_km)
    truck_derived = {'truck': {'mileage': {'liter-per-thousand-liter-km': {
        'value': liter_per_liter_km * 1000,
        'source': 'derived',
    }}}}
    with open('derived/transport.yaml', 'wt') as fp:
        yaml.dump(truck_derived, fp)

if __name__ == '__main__':
    main()

