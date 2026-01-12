from lib import create_circular_queue


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