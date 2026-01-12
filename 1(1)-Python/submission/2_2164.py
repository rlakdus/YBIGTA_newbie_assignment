from __future__ import annotations
from collections import deque


"""
TODO:
- rotate_and_remove 구현하기 
"""


def create_circular_queue(n: int) -> deque[int]:
    """1부터 n까지의 숫자로 deque를 생성합니다."""
    return deque(range(1, n + 1))

def rotate_and_remove(queue: deque[int], k: int) -> int:
    """
    큐의 원소를 이동시켜 k번째 원소를 제거하고 반환합니다.

    Args:
        - queue (deque[int]): 큐
        - k (int): 제거할 원소의 순서 

    Returns:
        - removed (int): 제거된 원소의 값
    """
    # 구현하세요!
    for _ in range(k - 1):
        queue.append(queue.popleft())
    return queue.popleft()
   




"""
TODO:
- simulate_card_game 구현하기
    # 카드 게임 시뮬레이션 구현
        # 1. 큐 생성
        # 2. 카드가 1장 남을 때까지 반복
        # 3. 마지막 남은 카드 반환
"""


def simulate_card_game(n: int) -> int:
    """
    큐를 생성한 후 카드가 1장 남을 때까지 매 반복마다 (1) 맨 위 카드를 버리고, (2) 그 다음 맨 위 카드를 맨 아래로 옮긴다.

    Args:
        - n (int): 카드의 개수 

    Returns:
        - last (int): 마지막에 남는 카드 번호
    """
    # 구현하세요!
    queue = create_circular_queue(n)

    while len(queue) > 1:
        queue.popleft()              
        queue.append(queue.popleft())  

    return queue[0]

def solve_card2() -> None:
    """입, 출력 format"""
    n: int = int(input())
    result: int = simulate_card_game(n)
    print(result)

if __name__ == "__main__":
    solve_card2()