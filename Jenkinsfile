pipeline{
    agent any

    triggers{
        githubPush()
    }

    stages{

        stage('Checkout'){
            steps{
                checkout scm
            }
        }
        stage('Install Dependencies'){
            steps{
                sh '''
            /opt/homebrew/bin/python3 -m venv .venv
            .venv/bin/python -m pip install --upgrade pip
            .venv/bin/pip install -r requirements.txt
        '''
            }
        }

        stage('Test'){
            steps{
                sh '''
            export PYTHONPATH="$WORKSPACE"
            .venv/bin/pytest
        '''
            }
        }
        stage('Build Docker Image'){
            steps{
                sh '''
            export PATH="/usr/local/bin:$PATH"
            /usr/local/bin/docker build -t naeomi/flask-app:latest .
        '''
            }
        }
        stage('Push to Docker Hub'){
            steps{
                withCredentials([
                    usernamePassword(
                        credentialsId:'dockerhub-cred',
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASS'
                    )
                ]){
                    sh '''
                        export PATH="/usr/local/bin:$PATH"
                        echo "$DOCKER_PASS"| /usr/local/bin/docker login -u "$DOCKER_USER" --password-stdin
                        /usr/local/bin/docker push naeomi/flask-app:latest
                    '''
                }
            }
        }
    }
   post {
        success {
            emailext(
                subject: "SUCCESS ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: """
                    <h2>Jenkins build Successful</h2>
                    <p>
                        <b>URL</b>: ${env.BUILD_URL}
                    </p>
                """,
                to: "naeomidias6@gmail.com"
            )
        }

        failure {
            emailext(
                subject: "FAILED ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: """
                    <h2>Jenkins build Failed</h2>
                    <p>
                        <b>URL</b>: ${env.BUILD_URL}
                    </p>
                """,
                to: "naeomidias6@gmail.com"
            )
        }
    }
} 
