pipeline {
    agent any

    environment {
        // Путь к твоему приложению
        APP_DIR = '.'
    }

    stages {
        stage('Checkout') {
            steps {
                // Забираем код из репозитория
                checkout scm
                echo 'Код успешно получен из GitHub'
            }
        }

        stage('Setup Environment') {
            steps {
                // Устанавливаем виртуальное окружение и зависимости
                dir(env.APP_DIR) {
                    bat '''
                        python -m venv venv
                        call venv\\Scripts\\activate.bat
                        python -m pip install --upgrade pip
                        python -m pip install -r requirements.txt
                    '''
                    echo 'Окружение настроено и зависимости установлены'
                }
            }
        }

        stage('Run Flask App') {
            steps {
                // Запускаем приложение в фоновом режиме
                dir(env.APP_DIR) {
                    bat '''
                        start /B call venv\\Scripts\\activate.bat && python app.py
                    '''
                }
                echo 'Flask-приложение запущено на http://localhost:5000'
            }
        }
    }

    post {
        // Действия после завершения сборки
        always {
            echo 'Pipeline завершен. Остановите Flask-приложение вручную, если это необходимо.'
        }
        failure {
            echo 'Pipeline завершился с ошибкой. Проверьте консольный вывод.'
        }
    }
}
