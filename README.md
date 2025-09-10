# Описание

Проект посвящен разработке модели для обнаружения изображений, сгенерированных нейросетями.
Цель - определить, насколько эффективно сверточные нейросети (CNN, ResNet) могут отличать реальные изображения от сгенерированных.

# Демо

https://ai-image-detector.ycalk.tech

# API Документация

https://ai-image-detector.ycalk.tech/api/docs

# Стек

Разработка модели
- PyTorch
- Torchvision
- Scikit-learn

Backend
- FastAPI
- FastStream
- RabbitMQ

Frontend
- React
- Mantine

# Компоненты
```
additional/ # Дополнительные компоненты
├── frontend/ # Fronted проекта
├── messaging_schema/ # Pydantic модели для обмена между сервисами
├── research/ # Исследование
│   └── README.md # Результаты исследования
services/
├── api/ # FastAPI приложение
├── detector/ # Сервис детектора
└── docker-compose.yaml # Сборка backend
```
---

<img width="2700" height="897" alt="410596331-f95b2897-f47e-452d-b76a-f484613cc164" src="https://github.com/user-attachments/assets/68045c71-6b03-4763-a65c-2b46deab1ba2" />
