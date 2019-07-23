from decimal import *
from simnm import NeutronMonitor, Sampler

eventos_por_minuto = 600
eventos_por_segundo = eventos_por_minuto / 60
beta = 1 / eventos_por_segundo
getcontext().prec = 9


def run():
    nm = NeutronMonitor(size=18, beta=beta)

    sampler = Sampler(Decimal("0.0000005"), nm)

    for sample in sampler.generator(Decimal("2.0")):
        print("{: >6d} {: >6d} [0x{}] {:12.6f}s - {} [0x{}]".format(
            sample['delta_steps'],
            sample['counter_steps'], (sample['counter_steps'] % pow(2, 32)).to_bytes(4, byteorder='big').hex(),
            sample['time_s'],
            sample['status_bin'], int(sample['status_bin'], 2).to_bytes(3, byteorder='big').hex())
        )


if __name__ == "__main__":
    run()
