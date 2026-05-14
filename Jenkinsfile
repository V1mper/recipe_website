pipeline {
    agent any

    environment {
        APP_DIR = '.'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
                echo 'Код успешно получен из GitHub'
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
                    echo 'Окружение настроено и зависимости установлены'
                }
            }
        }

        stage('Run Flask App') {
            steps {
                dir(env.APP_DIR) {
                    bat '''
                        call venv\\Scripts\\activate.bat
                        start /B python app.py > flask.log 2>&1
                        echo "Flask запущен, ждём 5 секунд..."
                        timeout /t 5 /nobreak > nul
                        for /f "tokens=*" %%i in ('netstat -ano ^| findstr :5000') do set line=%%i
                        if defined line (
                            echo "✅ Flask-сервер успешно запущен на порту 5000"
                        ) else (
                            echo "❌ Не удалось запустить Flask"
                            exit 1
                        )
                        echo "Останавливаем Flask..."
                        for /f "tokens=5" %%a in ('netstat -ano ^| findstr :5000 ^| findstr LISTENING') do taskkill /F /PID %%a
                    '''
                    echo "Flask-приложение протестировано и остановлено"
                }
            }
        }
    }

    post {
        always {
            echo 'Pipeline завершен.'
        }
        failure {
            echo 'Pipeline завершился с ошибкой. Проверьте консольный вывод.'
        }
    }
}
