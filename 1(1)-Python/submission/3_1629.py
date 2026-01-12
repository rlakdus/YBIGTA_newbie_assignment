# lib.py의 Matrix 클래스를 참조하지 않음
import sys


"""
TODO:
- fast_power 구현하기 
"""


def fast_power(base: int, exp: int, mod: int) -> int:
    """
    분할 거듭제곱을 이용해 base^exp%mod를 계산하는 함수.

    Args:
    - base (int): 밑이 되는 자연수 A
    - exp (int): 거듭제곱 횟수 B
    - mod (int): 나눌 값 C

    Returns:
    - result (int): base를 exp번 곱한 값을 mod로 나눈 나머지
    """
    # 구현하세요!
    result: int = 1
    base %= mod

    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % mod
        base = (base * base) % mod
        exp //= 2

    return result

def main() -> None:
    A: int
    B: int
    C: int
    A, B, C = map(int, input().split()) # 입력 고정
    
    result: int = fast_power(A, B, C) # 출력 형식
    print(result) 

if __name__ == "__main__":
    main()
