pipeline {
    agent any  // Run directly on the Jenkins host machine

    environment {
        DOCKER_IMAGE = "undefined014/django-app:latest"  // Docker image name
        REGISTRY_CREDENTIALS = credentials('docker')  // Docker credentials from Jenkins
    }

    stages {
        stage('Checkout') {
            steps {
                script {
                    echo "Cloning the repository"
                    git branch: 'main', url: 'https://github.com/manuCprogramming/spam-detection-project.git'
                }
            }
        }

        stage('Install Dependencies') {
            steps {
                script {
                    echo "Installing dependencies"
                    bat 'pip install -r requirements.txt'  // Windows batch command
                }
            }
        }

        /* stage('Static Code Analysis with SonarQube') {
            steps {
                script {
                    echo "Running static code analysis with SonarQube"
                    bat '''
                        docker run --rm ^
                        -v %CD%:/usr/src ^
                        sonarsource/sonar-scanner-cli:latest ^
                        -Dsonar.projectKey=Spam-Detection-Project ^
                        -Dsonar.sources=/usr/src ^
                        -Dsonar.host.url=http://host.docker.internal:9000 ^
                        -Dsonar.login=%sonarQ%
                    '''
                }
            }
        } */

        stage('Build and Push Docker Image') {
            steps {
                script {
                    echo "Checking if Docker is running..."
                    bat 'docker version || exit 1'

                    echo "Logging into Docker Hub"
                    bat 'echo %REGISTRY_CREDENTIALS_PSW% | docker login -u "%REGISTRY_CREDENTIALS_USR%" --password-stdin'

                    echo "Building Docker image"
                    bat "docker build -t ${env.DOCKER_IMAGE} ."

                    echo "Pushing Docker image to registry"
                    bat "docker push ${env.DOCKER_IMAGE}"
                }
            }
        }

        stage('Deploy Application') {
            steps {
                script {
                    echo "Checking Kubernetes cluster..."
                    bat 'kubectl cluster-info || exit 1'

                    echo "Deploying application to Kubernetes"
                    withCredentials([file(credentialsId: 'kubeconfig', variable: 'KUBECONFIG')]) {
                        bat '''
                            kubectl apply -f k8s/deployment.yaml
                            kubectl apply -f k8s/service.yaml
                        '''
                    }
                }
            }
        }
    }
}
