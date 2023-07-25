# HR Analytics - IBM HR Data

### Analysis Process
1. EDA 진행
    - 각 Feature별 datatype, nunique등 파악
    - Rank scale 성격의 variables의 경우 모델링의 편의를 위해 Ratio scale로 가정
    - EDA 진행하면서 일정 부분 실제 Data가 아닌 Randomized Data임을 확인
        - 불필요 Feature 삭제 : DailyRate, MonthlyRate 등 → MonthlyIncome만 남겨두는 형태
    - Continuous Features의 경우 kdeplot을 통해 분포 확인
    - Discrete Features의 경우 categorical로 astype하여 One-hot Encoding에 활용
    - 가공 Variables 추가 : 잦은 이직여부를 확인하는 Feature 등
2. 예측 정확도 등의 Baseline 설정
    - 별도의 Feature 전처리 없이 가볍게 확인
    - Baseline에서는 분석이 수반되지 않을 예정이므로 RandomForest를 주로 활용하여 Baseline 설정
    - Roc auc score 및 Confusion matrix 확인
    - 참고 차 Tree 모델을 이용한 Feature importance 확인 → 주로 어떤 사항이 Attrition에 영향을 미치는지
3. Factor Analysis 진행
    - Factor Analysis를 통해 대략적인 경향성을 파악
    - 단 roc_auc_score가 높지 않으므로 이후 다른 파일에서 각 Feature들을 세부적으로 뜯어서 분석
    - 전체 Variance의 60%가 넘도록 Factor의 수 설정
    - Factor loadings 확인 후 각 Feature들을 Factor에 배치 → Factor naming 진행
    - Factor loadings의 idxmax가 높지 않은 Feature들을 제거
    - 세부 분석을 위해 Logistic Regression 활용하여 모델링 진행
        - Roc auc score 및 Confusion matrix 확인 → RandomForest 모델과 비교
        - Coefficient 확인을 통하여 Attrition에 영향을 주는 요소 파악
        - Feature가 많지 않으므로 각 Feature에 대한 Significance Test 진행 → p_value 확인
            - statsmodel 라이브러리를 통한 재모델링 및 Coefficient 비교
    - 소결
        - 일정 부분 Randomized Data이므로 Factor Analysis의 효과가 크지는 않음
        - 대략적인 참고용으로만 확인


### Original Data Dictionary
* Age : 해당 직원의 나이
* Attrition : 퇴직 여부
* BusinessTravel : 출장의 빈도
* DailyRate : 일 대비 급여의 수준
* Department : 업무분야
* DistanceFromHome : 집과의 거리
* Education : 교육의 정도
    - 1 : ‘Below College’ : 대학 이하 / 2 : ‘College’ : 전문학사 / 3 : ‘Bachelor’ : 학사 / 4 : ‘Master’ : 석사 / 5 : ‘Doctor’ : 박사
* EducationField : 전공
* EmployeeCount : 직원 숫자
* EmployeeNumber : 직원 ID
* EnvironmentSatisfaction : 업무 환경에 대한 만족도
    - 1 : ‘Low’ / 2 : ‘Medium’ / 3 : ‘High’ / 4 : ‘Very High’
* Gender : 성별
* HourlyRate : 시간 대비 급여의 수준
* JobInvolvement : 업무 참여도
    - 1 : ‘Low’ / 2 : ‘Medium’ / 3 : ‘High’ / 4 : ‘Very High’
* JobLevel : 업무의 수준
* JobRole : 업무 종류
* JobSatisfaction : 업무 만족도
    - 1 : ‘Low’ / 2 : ‘Medium’ / 3 : ‘High’ / 4 : ‘Very High’
* MaritalStatus : 결혼 여부
* MonthlyIncome : 월 소득
* MonthlyRate : 월 대비 급여 수준
* NumCompaniesWorked : 일한 회사의 수
* Over18 : 18세 이상
* OverTime : 규정외 노동시간
* PercentSalaryHike : 급여의 증가분 백분율
* PerformanceRating : 업무 성과
    - 1 : ‘Low’ / 2 : ‘Good’ / 3 : ‘Excellent’ / 4 : ‘Outstanding’
* RelationshipSatisfaction : 대인관계 만족도
    - 1 : ‘Low’ / 2 : ‘Medium’ / 3 : ‘High’ / 4 : ‘Very High’
* StandardHours : 표준 시간
* StockOptionLevel : 스톡옵션 정도
* TotalWorkingYears : 경력 기간
* TrainingTimesLastYear : 교육 시간
* WorkLifeBalance : 일과 생활의 균형 정도
    - 1 : ‘Bad’ / 2 : ‘Good’ / 3 : ‘Better’ / 4 : ‘Best’
* YearsAtCompany : 근속 연수
* YearsInCurrentRole : 현재 역할의 년수
* YearsSinceLastPromotion : 마지막 프로모션
* YearsWithCurrManager : 현재 관리자와 함께 보낸 시간