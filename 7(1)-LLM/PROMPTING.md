# LLM 과제 - Prompting

## 0. Overview
이번 과제의 목표는 프롬프트 설계 방식에 따라 대형 언어 모델의 추론 성능이 어떻게 달라지는지 분석하는 것이다.
- 데이터셋: GSM8K 
- 모델: Llama 3.1 8b Instant

## 1. Results 

아래 표는 Direct Prompting, CoT Prompting, 그리고 새로운 프롬프트(My Prompting)에 대해
0-shot, 3-shot, 5-shot 설정에서의 정답률을 비교한 결과이다.


| Prompting Method | 0-shot Acc. | 3-shot Acc. | 5-shot Acc. |
|------------------|-------------|-------------|-------------|
| Direct Prompting | 80% | 76% | 78% |
| CoT Prompting | 82% | 76% | 82% |
| My Prompting | 86% | 88% | 84% |


<img width="630" height="470" alt="Image" src="https://github.com/user-attachments/assets/a3b4369c-e598-41da-920e-e646dfea4430" />


- Direct Prompting:
3-shot < 5-shot < 0-shot

- CoT Prompting:
0-shot과 5-shot에서 Direct Prompting 대비 정답률이 소폭 상승하였다.

- My Prompting:
CoT와 Direct 대비 성능이 전반적으로 향상된 걸 확인할 수 있다.


## 2. Discussion

### 2-1. Direct Prompting vs CoT Prompting 

Direct Prompting은 모델에게 최종 정답만 출력하도록 요구하기 때문에, GSM8K와 같이 추론이 필요한 문제에서 중간 계산 과정이 출력으로 드러나지 않는다. 
이로 인해 모델이 내부적으로 추론 중 실수를 하더라도 이를 수정할 기회가 제한되며, 결과적으로 정답률이 낮게 나타나는 경향이 있다.

반면, CoT Prompting은 문제 해결 과정을 단계별로 서술하도록 유도하기 때문에 모델이 계산을 명시적으로 수행하면서 추론을 어느정도 안정적으로 할 수 있게 한다.
우리가 수학 문제를 풀때처럼 모델이 각 단계를 서술하면서 이전 단계의 결과를 참조하고 확인할 수 있기 때문에 일종의 implicit self-verification을 할 수 있게된다. 
또한, Few-shot 예시를 주면 모델이 올바른 추론 패턴을 학습하면서 테스트 데이터 추론 시 유사한 문제 구조를 인식하고 적절한 해결 전략을 적용할 가능성이 높아진다.

하지만 이번 과제의 실험 결과를 토대로 CoT Prompting이 항상 Direct Prompting보다 우수한 성능을 보인다고 단정할 수는 없을 것 같다. 
최근 대규모 언어 모델은 사전학습 및 지시 튜닝 과정에서 이미 다양한 추론 패턴을 내재화하고 있으며, 이로 인해 중간 추론 과정을 명시적으로 출력하지 않더라도 내부적으로 충분한 추론을 수행할 수 있는 능력을 갖추게 되었기 때문에 direct의 성능이 크게 좋아진 것으로 보인다.

### 2-2. Effect of Few Shots
Few-shot prompting은 모델에게 예시를 줌으로서 형식을 파악하도록 돕는 역할을 한다.  
Direct Prompting에서는 few-shot 예시가 추가되더라도 성능 향상이 일관되게 나타나지 않았다. 
Direct Prompting은 모델이 문제를 보고 최종 정답만 생성하도록 하기 때문에 최종 정답만 예시로 주는 것은 크게 의미가 없을 것이라 예상된다. 
반면, CoT Prompting과 My Prompting에서는 few-shot이 제공되면 모델이 reasoning의 구조와 답안 형식을 학습하면서 성능이 향상하리라 예상했다. 하지만 실험 결과 0-shot에서도 모델들이 충분히 좋은 성능을 보였고, 마찬가지로 모델 자체의 추론 능력이 이미 높아 크게 효과가 없을 수도 있을 것이다. 

### 2-3. My Prompt
1. 역할 부여: 프롬프트의 시작 부분에서 모델에게 수학 전문가(math expert)라는 페르소나를 부여하였다. 

2. 명확한 문제 이해:
수학적 계산에 들어가기 전에 문제를 정확히 이해하도록 지시하였다. GSM8K는 자연어로 서술된 수학 문제이기 때문에, 계산 자체보다 문제의 맥락과 조건을 올바르게 해석하는 것이 중요하다고 생각했다. 문제의 맥락만 정확히 파악된다면, 계산 과정 자체는 문제 난이도가 쉽기 때문에 모델이 잘 수행할 수 있을 것이라 생각하였다.
실제로 다음 논문에서는 GSM8K의 오류 유형을 분석한 결과, semantic misunderstanding이 가장 큰 오류 유형으로 나타난다. (https://arxiv.org/html/2404.14963v5)
이를 참고하여 프롬프트에 “no semantic misunderstanding is allowed”와 같이 강한 표현을 사용함으로써 모델이 문제의 문맥을 잘못 이해하는 오류를 최대한 줄이고자 하였다.

3. Chain-of-Thought(CoT):
문제를 해결하는 과정에서는 기존에 사용하던 CoT 방식을 그대로 유지하였다.

4. 출력 형식 지정:
최종 정답은 반드시 training dataset과 동일한 형식인 #### <number> 형태로 출력하도록 명시하였다. extract_final_answer 함수에도 이를 반영하여 정답을 추출할 수 있도록 하였다.


위와 같이 설계한 프롬프트가 기존 CoT Prompting보다 성능이 더 높게 나타날 수 있었던 이유는 문제 이해 부분에 있다고 생각한다. Direct Prompting과 CoT Prompting의 결과를 모델이 reasoning 자체는 이미 잘 수행하고 있다고 생각하였다.

따라서 성능을 추가로 향상시키기 위해서는 모델이 자신의 reasoning을 점검하고 오류를 잡아내는 능력이 중요하다고 생각하여 초기에는 모델에게 풀이를 점검하고 오류를 잡아내도록 프롬프트를 설계하였다.
그러나 성능 향상이 크지 않아, 보다 구체적인 오류 원인을 명시할 필요가 있다고 판단하여 문제의 맥락을 명확히 파악하도록 유도하는 방향으로 프롬프트를 설계하게 되었다.
특히, 추론 이후에 다시 확인하는 방식보다는, 문제를 해결하기 전에 먼저 계획하고 이해하는 과정이 선행되는 것이 더 자연스럽다고 생각하여 모델이 plan → solve의 순서로 문제를 해결하도록 유도하였다.
또한, 프롬프트를 설계하는 과정에서 이미 성능이 좋은 모델에 대해 과도하게 복잡한 지시를 추가하기보다는 token limit 등을 고려하여 최대한 단순한 구조를 유지하고자 하였다. 
결과적으로, 명확한 역할과 핵심적인 지시만으로도 성능이 크지는 않지만 일정 수준 향상되는 것을 확인할 수 있었다.
