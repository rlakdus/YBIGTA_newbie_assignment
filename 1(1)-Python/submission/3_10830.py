from __future__ import annotations
import copy


"""
TODO:
- __setitem__ 구현하기
- __pow__ 구현하기 (__matmul__을 활용해봅시다)
- __repr__ 구현하기
"""


class Matrix:
    MOD = 1000

    def __init__(self, matrix: list[list[int]]) -> None:
        self.matrix = matrix

    @staticmethod
    def full(n: int, shape: tuple[int, int]) -> Matrix:
        return Matrix([[n] * shape[1] for _ in range(shape[0])])

    @staticmethod
    def zeros(shape: tuple[int, int]) -> Matrix:
        return Matrix.full(0, shape)

    @staticmethod
    def ones(shape: tuple[int, int]) -> Matrix:
        return Matrix.full(1, shape)

    @staticmethod
    def eye(n: int) -> Matrix:
        matrix = Matrix.zeros((n, n))
        for i in range(n):
            matrix[i, i] = 1
        return matrix

    @property
    def shape(self) -> tuple[int, int]:
        return (len(self.matrix), len(self.matrix[0]))

    def clone(self) -> Matrix:
        return Matrix(copy.deepcopy(self.matrix))

    def __getitem__(self, key: tuple[int, int]) -> int:
        return self.matrix[key[0]][key[1]]

    def __setitem__(self, key: tuple[int, int], value: int) -> None:
        # 구현하세요!
        '''
        행렬의 특정 위치에 값을 대입하는 메소드.
        이때, 저장되는 값은 MOD로 나눈 후 나머지 값
        
        Args:
        - key (tuple[int, int]): (행, 열) 형태의 인덱스.
        - value (int): 해당 위치에 저장할 정수 값.
        
        Returns:
        - None
        '''
        r, c = key
        self.matrix[r][c] = value % self.MOD

    def __matmul__(self, matrix: Matrix) -> Matrix:
        x, m = self.shape
        m1, y = matrix.shape
        assert m == m1

        result = self.zeros((x, y))

        for i in range(x):
            for j in range(y):
                for k in range(m):
                    result[i, j] += self[i, k] * matrix[k, j]

        return result

    def __pow__(self, n: int) -> Matrix:
        # 구현하세요!
        '''
        matmul 메소드를 사용하여 행렬의 거듭제곱을 계산하는 메소드.
        빠른 계산을 위해 분할 거듭제곡 사용
        행렬은 반드시 정사각 행렬
        
        Args:
        - n (int): 거듭제곱 지수.
        
        Returns:
        - result (Matrix): 현재 행렬을 n제곱한 결과 행렬.
        '''
        assert self.shape[0] == self.shape[1]
        
        result = Matrix.eye(self.shape[0])
        base = self.clone()
        
        while n > 0:
            if n % 2 == 1:
                result = result @ base
            base = base @ base
            n //= 2 
        return result

    def __repr__(self) -> str:
        # 구현하세요!
        '''
        행렬을 문자열 형태로 표현하는 메소드.
        각 행은 한 줄로 출력하고, 원소는 공백으로 구분한다.

        Args:
        - 없음

        Returns:
        - s (str): 행렬을 행 단위로 출력한 문자열
        '''
        lines = []
        for row in self.matrix:
            line = ""
            for x in row:
                line += str(x % self.MOD) + " "
            lines.append(line.strip()) 
        
        return "\n".join(lines)
    


from typing import Callable
import sys


"""
-아무것도 수정하지 마세요!
"""


def main() -> None:
    intify: Callable[[str], list[int]] = lambda l: [*map(int, l.split())]

    lines: list[str] = sys.stdin.readlines()

    N, B = intify(lines[0])
    matrix: list[list[int]] = [*map(intify, lines[1:])]

    Matrix.MOD = 1000
    modmat = Matrix(matrix)

    print(modmat ** B)


if __name__ == "__main__":
    main()