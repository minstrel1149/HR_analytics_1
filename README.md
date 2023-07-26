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
4. 세부 모델링 진행
    - PolynomialFeatures를 통한 Feature 확장(interaction_only=True로 설정)
        - Feature들이 Multicolinearity를 가질 수 밖에 없으므로, 연결된 요소 파악하기 위한 방안
    - 세부 분석을 위해 Logistic Regression 활용하여 모델링 진행
        - Feature 확장으로 인해 Feature가 많아진 부분 고려 → L1 Regularization 수행
        - 영향을 주는 Feature들의 수를 줄이기 위해 Regularization 강화
        - Baseline보다 더 높은 Roc auc score 획득 → cutoff 조정에 활용
    - Confusion matrix 확인 및 cutoff 조정(0.65)
        - 최대한 Accuracy가 유지되는 선에서 Attrition 할 것이란 예측을 극대화
    - 일정 수준 이상 영향을 주는 Coefficient 확인 및 주요 영향 내용 정리
        - negative 영향(Attrition X) : Age-JobInvolvement / HighWLB
        - positive 영향(Attrition O) : LowEnvSatis-FreqMove / FreqMove-LowWLB / FreqMove-Sales / Single-LowWLB
5. 재직인원 Attrition 예상자 Clustering 진행
    - 거리 기반 Clustering(K-Means, Ward method 등)을 진행할 예정이므로 StandardScaler 필수 진행
        - Scaler의 학습은 전체 Dataset을 대상으로 진행 → 전체 대비 Attrition 예상자의 수치 파악
    - 세부 모델링에서 나온 Coefficient 기반으로 유의미한 Feature들만 추출하여 Feature 확인
    - 모델링한 Feature들에 대하여 좀 더 손쉬운 파악을 위해 Factor analysis 적용
        - Variance 설명량이 80%가 넘도록 Factor의 수 설정
        - 각 Factor들 Naming으로 이해 용이하도록 조치
    - K-Means, Hierachical Clustering(Ward method)를 바탕으로 Cluster 확인
        - Elbow, Calinski-Harabasz, Dendrogram 고려 후 Hierachical Clustering 선택
        - 예측된 Cluster들을 Factor Analysis 완료된 DataFrame에 할당
    - Clustering 자료 분석 결과 정리
        - cluster 0 : Age, JobInvolvement, WLB 등에 문제가 생긴 케이스
        - cluster 1 : 세부 조사가 필요한 다양한 이유(단, 기존 재직 회사가 많지 않은 편)
        - cluster 2 : Age, JobInvolvement가 강함에도 다양한 문제가 생긴 케이스
        - cluster 3 : Performance가 떨어지는 케이스
        - cluster 4 : Technician 쪽에서 OverTime이 잦은 케이스
        - cluster 5 : 최근 승진이 오래된 케이스
        - cluster 6 : Sales 쪽에서 이직이 잦았으며, 워라밸이 안좋은 케이스

### 고려할 점/느낀 점
* 일정 부분 Randomized된 Data이므로, 예측이 아닌 세부 분석에 있어서는 다소간 부정확한 부분 존재
    - 실제 Data를 활용할 시 훨씬 더 정확/정교하게 분석이 가능할 것으로 예상
* 퇴직 예상자에 대한 Clustering 진행 시, 확장된 Feature를 활용하기보다는 원본 Data의 Feature를 활용하는 것이 좀 더 효과적일듯
* Factor Analysis는 세부 내용 분석에 많은 기여 → HR 도메인 지식 바탕으로 적극적으로 활용 필요
* (중요!) 퇴직 분석의 경우 대상자의 기간을 두고 Train Dataset을 구성하는 것이 필요
    - 중요한 점은 결국 내부 대상자 중에 어떤 그룹이 퇴직할 것인가를 파악하는 것
    - 단순히 전체 데이터를 Random으로 Train dataset과 Test dataset으로 배치하면 분석에 좀 더 어려움을 겪을 가능성
    - 예시 : Train dataset → 5년 이상 재직자 + 전체 퇴직자 / Test dataset → 5년 이하 재직자
        - 이렇게 활용하면 5년 이하 재직자 중 회사를 오래 다닐 가능성이 낮은 인원들을 파악 가능
        - 해당 인원들이 어떠한 이유로 보통 퇴사를 선택하게 되는지 세부 분석 가능
        - 기간은 각 회사의 상황에 맞게 유동적으로 설정 가능
* 결론 : HR Data Analysis의 의미를 찾기 위해서는 HR 도메인 지식과 Data Analytics의 지식이 모두 필요

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