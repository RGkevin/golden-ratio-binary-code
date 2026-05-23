import math

PHI = (1 + math.sqrt(5)) / 2
SQRT5 = math.sqrt(5)


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

    Positional values are Fibonacci numbers F1=1, F2=1, F3=2, F4=3, F5=5, ...
    The representation is built from the fractal block structure defined in
    GOLDEN_RATIO_BINARY_CODE.md.

    Args:
        n: A positive integer.

    Returns:
        A string of '0' and '1' representing n in golden-ratio binary.

    Examples:
        >>> to_golden_ratio_binary(1)
        '1'
        >>> to_golden_ratio_binary(5)
        '1011'
        >>> to_golden_ratio_binary(8)
        '10101'
    """
    if not isinstance(n, int) or n <= 0:
        raise ValueError("n must be a positive integer")

    fibs = _generate_fibs(n)
    b = find_block(n, fibs)
    pos = n - fibs[b]  # 0-indexed position within block b
    return _encode_block(b, pos, fibs)
