#!/bin/bash

# anaconda(또는 miniconda)가 존재하지 않을 경우 설치해주세요!
## TODO
if [ -f "$HOME/miniconda3/etc/profile.d/conda.sh" ]; then
    source "$HOME/miniconda3/etc/profile.d/conda.sh"
else
    echo "[ERROR] conda.sh를 찾을 수 없습니다."
    exit 1
fi

conda --version

# Conda 환셩 생성 및 활성화
## TODO
conda create -n myenv python=3.11 -y || true
conda activate myenv

## 건드리지 마세요! ##
python_env=$(python -c "import sys; print(sys.prefix)")
if [[ "$python_env" == *"/envs/myenv"* ]]; then
    echo "[INFO] 가상환경 활성화: 성공"
else
    echo "[INFO] 가상환경 활성화: 실패"
    exit 1 
fi

# 필요한 패키지 설치
## TODO
pip install mypy

# Submission 폴더 파일 실행
cd submission || { echo "[INFO] submission 디렉토리로 이동 실패"; exit 1; }

for file in *.py; do
    ## TODO
    filename=$(basename "$file" .py)
    problem=${filename#*_}

    python "$file" < "../input/${problem}_input" > "../output/${problem}_output"
done

# mypy 테스트 실행 및 mypy_log.txt 저장
## TODO
mypy *.py > ../mypy_log.txt

# conda.yml 파일 생성
## TODO
conda env export > ../conda.yml

# 가상환경 비활성화
## TODO
conda deactivate