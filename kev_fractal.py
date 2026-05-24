from dataclasses import dataclass

from golden_ratio_binary_code import _generate_fibs, find_block, to_golden_ratio_binary_iterative


@dataclass
class FractalEntry:
    n: int
    block: int
    bits: str
    is_prime: bool

    def bit_count(self) -> int:
        return self.bits.count("1")


def _is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(n ** 0.5) + 1, 2):
        if n % i == 0:
            return False
    return True


def build_kev_fractal(max_n: int = 143) -> list[FractalEntry]:
    """Build 'El Fractal de Kev' for N = 1 .. max_n."""
    fibs = _generate_fibs(max_n)
    return [
        FractalEntry(
            n=n,
            block=find_block(n, fibs),
            bits=to_golden_ratio_binary_iterative(n),
            is_prime=_is_prime(n),
        )
        for n in range(1, max_n + 1)
    ]


if __name__ == "__main__":
    fractal = build_kev_fractal()

    print(f"{'N':>4} | {'Block':>5} | {'Bits':<12} | {'Prime':>5}")
    print("-" * 36)
    for e in fractal:
        print(f"{e.n:>4} | {e.block:>5} | {e.bits:<12} | {str(e.is_prime):>5}")
