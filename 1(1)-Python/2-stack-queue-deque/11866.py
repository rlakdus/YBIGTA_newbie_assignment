from lib import create_circular_queue, rotate_and_remove


"""
TODO:
- josephus_problem 구현하기
    # 요세푸스 문제 구현
        # 1. 큐 생성
        # 2. 큐가 빌 때까지 반복
        # 3. 제거 순서 리스트 반환
"""


def josephus_problem(n: int, k: int) -> list[int]:
    """
    n명의 사람이 원을 이루고 있을 때, k번째 사람을 반복적으로 제거하고 그 제거되는 순서를 리스트로 반환한다.

    Args:
        - n (int): 사람의 수 
        - k (int): 제거할 순서 

    Returns:
        - order (list[int]): 사람들이 제거되는 순서
    """
    # 구현하세요!
    queue = create_circular_queue(n)
    result: list[int] = []

    while queue:
        removed = rotate_and_remove(queue, k)
        result.append(removed)

    return result

def solve_josephus() -> None:
    """입, 출력 format"""
    n: int
    k: int
    n, k = map(int, input().split())
    result: list[int] = josephus_problem(n, k)
    
    # 출력 형식: <3, 6, 2, 7, 5, 1, 4>
    print("<" + ", ".join(map(str, result)) + ">")

if __name__ == "__main__":
    solve_josephus()