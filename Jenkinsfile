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
