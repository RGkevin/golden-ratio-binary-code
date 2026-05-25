import math

PHI = (1 + math.sqrt(5)) / 2
SQRT5 = math.sqrt(5)

_FIB_CACHE: list[int] = [1, 1]


def _get_fibs_cached(n: int) -> list[int]:
    while _FIB_CACHE[-1] <= n:
        _FIB_CACHE.append(_FIB_CACHE[-1] + _FIB_CACHE[-2])
    return _FIB_CACHE


def _generate_fibs(n: int) -> list[int]:
    """Returns [F1=1, F2=1, F3=2, ...] with enough terms to cover n."""
    fibs = [1, 1]
    while fibs[-1] <= n:
        fibs.append(fibs[-1] + fibs[-2])
    return fibs


def find_block(n: int, fibs: list[int]) -> int:
    """
    Returns block index b (1-based) where n lives.

    Block b starts at F_{b+1} = fibs[b] and has F_b = fibs[b-1] elements.
    Uses the O(1) golden-ratio formula from the document with a boundary
    correction to handle floating-point edge cases near Fibonacci numbers.
    """
    if n == 1:
        return 1
    argumento = (n + 1) * SQRT5
    b = int(math.log(argumento) / math.log(PHI)) - 1
    # Correct downward if the estimate overshot (boundary FP issue)
    while b > 1 and fibs[b] > n:
        b -= 1
    # Correct upward if the estimate undershot
    while b + 1 < len(fibs) and fibs[b + 1] <= n:
        b += 1
    return b


def _encode_block(b: int, pos: int, fibs: list[int]) -> str:
    """
    Returns the bit string for the pos-th element (0-indexed) of block b.

    Recursive structure (b >= 3):
      block_b = [ "10" + block_{b-2} ]   <- first F_{b-2} elements
             ++ [ "1"  + block_{b-1} ]   <- next  F_{b-1} elements
    Base cases:
      block_1 = ["1"]
      block_2 = ["11"]
    """
    if b == 1:
        return "1"
    if b == 2:
        return "11"

    f_b_minus_2 = fibs[b - 3]  # F_{b-2}: size of the first sub-block

    if pos < f_b_minus_2:
        return "10" + _encode_block(b - 2, pos, fibs)
    return "1" + _encode_block(b - 1, pos - f_b_minus_2, fibs)


def to_golden_ratio_binary(n: int) -> str:
    """
    Convert a natural number to its golden-ratio binary (Fibonacci base) string.

    Uses the recursive fractal block structure (see GOLDEN_RATIO_BINARY_CODE.md).

    Examples:
        >>> to_golden_ratio_binary(5)
        '1011'
    """
    if not isinstance(n, int) or n <= 0:
        raise ValueError("n must be a positive integer")

    fibs = _generate_fibs(n)
    b = find_block(n, fibs)
    pos = n - fibs[b]  # 0-indexed position within block b
    return _encode_block(b, pos, fibs)


def _iter_block_bits(b: int, fibs: list[int], prefix: str = "") -> "Generator[str, None, None]":
    if b == 1:
        yield prefix + "1"
        return
    if b == 2:
        yield prefix + "11"
        return
    yield from _iter_block_bits(b - 2, fibs, prefix + "10")
    yield from _iter_block_bits(b - 1, fibs, prefix + "1")


def encode_block(b: int) -> list[tuple[int, str]]:
    """
    Return [(n, bits), ...] for every number in block b, in order.

    Uses the fractal block structure to generate all codes sharing a single
    Fibonacci table — much faster than calling to_golden_ratio_binary per element.

    Example:
        >>> encode_block(4)
        [(5, '1011'), (6, '1101'), (7, '1111')]
    """
    if b < 1:
        raise ValueError("b must be >= 1")
    fibs: list[int] = [1, 1]
    while len(fibs) <= b + 1:
        fibs.append(fibs[-1] + fibs[-2])
    block_start = fibs[b]
    return [(block_start + i, bits) for i, bits in enumerate(_iter_block_bits(b, fibs))]


def to_golden_ratio_binary_iterative(n: int) -> str:
    """
    Convert a natural number to its golden-ratio binary string without recursion.

    The recursive block structure unfolds into a single while loop.  At each
    step the two-variable state (b, pos) shrinks by at least 1, so the loop
    runs O(log_φ N) iterations.

    At every iteration we decide:
      - pos < F_{b-2}  →  emit "10", jump to block b-2 (skip one level)
      - pos >= F_{b-2} →  emit "1",  jump to block b-1 (step one level down)

    The emitted fragments, concatenated in order, form the final bit string.

    Examples:
        >>> to_golden_ratio_binary_iterative(5)
        '1011'
    """
    if not isinstance(n, int) or n <= 0:
        raise ValueError("n must be a positive integer")

    fibs = _generate_fibs(n)
    b = find_block(n, fibs)
    pos = n - fibs[b]  # 0-indexed position within block b

    parts: list[str] = []
    while b > 2:
        f_b_minus_2 = fibs[b - 3]  # F_{b-2}: size of the left sub-block
        if pos < f_b_minus_2:
            parts.append("10")
            b -= 2
        else:
            parts.append("1")
            pos -= f_b_minus_2
            b -= 1

    parts.append("11" if b == 2 else "1")
    return "".join(parts)
