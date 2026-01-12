from __future__ import annotations
import copy
from collections import deque
from collections import defaultdict
from typing import DefaultDict, List


"""
TODO:
- __init__ 구현하기
- add_edge 구현하기
- dfs 구현하기 (재귀 또는 스택 방식 선택)
- bfs 구현하기
"""


class Graph:
     
    def __init__(self, n: int) -> None:
        """
        그래프 초기화
        n: 정점의 개수 (1번부터 n번까지)
        """
        self.n: int = n
        self.adj: DefaultDict[int, List[int]] = defaultdict(list)

    
    def add_edge(self, u: int, v: int) -> None:
        """
        그래프에 양방향 간선을 추가한다.

        Args: 
        - u (int): 간선의 한쪽 정점 번호
        - v (int): 간선의 다른 한쪽 정점 번호

        Returns:
        - None
        """
        # 구현하세요!
        self.adj[u].append(v)
        self.adj[v].append(u)
    
    def dfs(self, start: int) -> list[int]:
        """
        깊이 우선 탐색 (DFS)
        
        재귀 방식을 사용하여 탐색한다.

        Args
        - start (int): 탐색을 시작할 정점 번호 정의

        Returns ()
        - result (list[int]): DFS 탐색 순서가 저장된 리스트
        """
        # 구현하세요!
        path = [False] * (self.n + 1)
        result: list[int] = []

        def _dfs(u: int) -> None:
            path[u] = True
            result.append(u)
            for v in sorted(self.adj[u]):
                if not path[v]:
                    _dfs(v)

        _dfs(start)
        return result

    
    def bfs(self, start: int) -> list[int]:
        """
        너비 우선 탐색 (BFS)

        큐(deque)를 사용하여 탐색한다.

        Args
        - start(int): 탐색을 시작할 정점 번호

        Returns
        - result (list[int]): BFS 탐색 순서가 저장된 리스트
        """
        # 구현하세요!
        path = [False] * (self.n + 1)
        result: list[int] = []
        q = deque([start])
        path[start] = True

        while q:
            u = q.popleft()
            result.append(u)
            for v in sorted(self.adj[u]):
                if not path[v]:
                    path[v] = True
                    q.append(v)

        return result
    
    def search_and_print(self, start: int) -> None:
        """
        DFS와 BFS 결과를 출력
        """
        dfs_result = self.dfs(start)
        bfs_result = self.bfs(start)
        
        print(' '.join(map(str, dfs_result)))
        print(' '.join(map(str, bfs_result)))



from typing import Callable
import sys


"""
-아무것도 수정하지 마세요!
"""


def main() -> None:
    intify: Callable[[str], list[int]] = lambda l: [*map(int, l.split())]

    lines: list[str] = sys.stdin.readlines()

    N, M, V = intify(lines[0])
    
    graph = Graph(N)  # 그래프 생성
    
    for i in range(1, M + 1): # 간선 정보 입력
        u, v = intify(lines[i])
        graph.add_edge(u, v)
    
    graph.search_and_print(V) # DFS와 BFS 수행 및 출력


if __name__ == "__main__":
    main()
