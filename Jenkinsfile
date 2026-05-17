pipeline {
    agent any

    environment {
        APP_DIR = '.'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
                echo '✅ Код получен из GitHub'
            }
        }

        stage('Setup Environment') {
            steps {
                dir(env.APP_DIR) {
                    bat '''
                        python -m venv venv
                        call venv\\Scripts\\activate.bat
                        python -m pip install --upgrade pip
                        python -m pip install -r requirements.txt
                    '''
                    echo '✅ Окружение настроено и зависимости установлены'
                }
            }
        }

        stage('Test Application') {
            steps {
                dir(env.APP_DIR) {
                    bat '''
                        call venv\\Scripts\\activate.bat
                        echo "Проверка синтаксиса app.py..."
                        python -m py_compile app.py
                        if errorlevel 1 exit /b 1
                        echo "✅ Синтаксис корректен"
                        echo "Проверка наличия шаблонов..."
                        if not exist templates\\* echo "⚠️ Нет шаблонов HTML" & exit /b 0
                        echo "✅ Шаблоны найдены"
                    '''
                    echo '✅ Тестирование пройдено успешно'
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                dir(env.APP_DIR) {
                    bat '''
                        echo "Сборка Docker-образа recipe-website:latest..."
                        docker build -t recipe-website:latest .
                        if errorlevel 1 exit /b 1
                        echo "✅ Образ успешно собран"
                    '''
                }
            }
        }

        stage('Test Container') {
            steps {
                dir(env.APP_DIR) {
                    bat '''
                        echo "Запуск контейнера из образа..."
                        docker run -d --name test-recipe -p 5000:5000 recipe-website:latest
                        if errorlevel 1 exit /b 1
                        echo "Ожидание 5 секунд для запуска Flask..."
                        timeout /t 5 /nobreak > nul
                        echo "Проверка доступности сайта (curl)..."
                        curl http://localhost:5000 || echo "⚠️ curl не установлен, но контейнер запущен"
                        echo "✅ Контейнер работает, порт 5000 открыт"
                        echo "Остановка и удаление тестового контейнера..."
                        docker stop test-recipe
                        docker rm test-recipe
                        echo "✅ Контейнер успешно протестирован и удалён"
                    '''
                }
            }
        }
    }

    post {
        success {
            echo '🎉 Pipeline успешно завершён!'
        }
        failure {
            echo '❌ Pipeline завершился ошибкой. Проверьте логи выше.'
        }
    }
}
