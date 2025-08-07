# 🚢 선박 컨테이너 자동 온습도 관리 시스템

📌 **운송 중 컨테이너 내부의 온도와 습도를 자동으로 조절하여 화물의 품질을 안전하게 유지하는 스마트 관리 시스템**

---

## ✨ 시연영상

https://www.youtube.com/watch?v=cBYhsSrshSg

---

## 🔧 기술 스택

<img src="https://img.shields.io/badge/C-A8B9CC?style=for-the-badge&logo=C&logoColor=white">  
<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=Python&logoColor=white">  
<img src="https://img.shields.io/badge/PyQt5-41CD52?style=for-the-badge&logo=Qt&logoColor=white">  
<img src="https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=MySQL&logoColor=white">  
<img src="https://img.shields.io/badge/STM32-03234B?style=for-the-badge&logo=stmicroelectronics&logoColor=white">  
<img src="https://img.shields.io/badge/raspberrypi-A22846?style=for-the-badge&logo=raspberrypi&logoColor=white">

---

## 📸 소개

컨테이너 운송 과정에서 외부 기후 변화로 인해 내부 환경이 급격하게 변할 수 있습니다.  
이 프로젝트는 **STM32 마이크로컨트롤러와 라즈베리파이, Bluetooth, GUI 애플리케이션**을 기반으로  
컨테이너 내부의 온도와 습도를 **실시간으로 측정 및 제어**하는 자동화 시스템입니다.  
운송 화물의 품질과 안전을 유지하기 위해 **관리자 개입 없이도** 이상 상황을 감지하고 자동으로 대응합니다.

- **개발 기간:** 2024.04.08 ~ 2024.05.07  
- **참여 인원:** 4명

---

## 🚀 주요 기능

### ✅ `Container_STM`
- 실시간 온습도 센서 제어 및 수집
- Bluetooth 모듈을 통해 측정된 데이터를 Raspberry Pi에 송신

### ✅ `Container_GUI`
- 수신된 온습도 데이터를 **MySQL DB에 저장** 및 **CSV 파일 저장**
- 수신 데이터를 **PyQt5 기반 GUI에 실시간 시각화**
- 관리자 요청에 따라 **컨테이너 내부의 온습도 경계값 설정/전송** 가능

---

## 🔁 시스템 플로우차트

<img width="662" height="471" alt="FlowChart" src="https://github.com/user-attachments/assets/f84adbc4-ba2a-49e4-85c4-32fba5383f28" />

---

## 🖥️ GUI 화면

<img width="683" height="364" alt="GUI" src="https://github.com/user-attachments/assets/02b960d4-87c7-462b-8a81-3b92da240a8a" />

---


## 📄 라이선스

이 프로젝트는 MIT 라이선스를 따릅니다.  
자세한 내용은 `LICENSE` 파일을 참고하세요.

---

## 📧 연락처

- **안진홍** - [ajh9703@gmail.com](mailto:ajh9703@gmail.com)

---
