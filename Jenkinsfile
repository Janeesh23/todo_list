pipeline{
    agent any

    environment {
        registrycredential = 'ecr:us-east-1:awscreds'
        imagename = "540502631636.dkr.ecr.us-east-1.amazonaws.com/flaskappimg"
        registryurl = "https://540502631636.dkr.ecr.us-east-1.amazonaws.com"
        cluster = 'Todo_app'
        service = 'TODOSVC'
    }

    stages{
        stage('FETCH CODE'){
            steps{
                git branch: 'main', url: 'https://github.com/Janeesh23/todo_list.git'
            }
        }

        stage('Setup Python Environment & Install Dependencies') {
            steps {
                sh '''
                if [ ! -d "venv" ]; then
                    python3 -m venv venv
                fi
                . venv/bin/activate
                python3 -m pip install --upgrade pip
                pip install --cache-dir=/var/cache/pip -r requirements.txt
                '''
            }
        }

        stage('RUN TESTS'){
            steps{
                    sh '''
                    . venv/bin/activate
                    pytest tests/
                    '''
            }
            post{
                success{
                    echo "all tests passed...moving to the build process"
                }

                failure{
                    echo "failed the tes cases"
                    error('stoppping the pipeline due to test failures')
                }
            }
        }

        stage('BUILD THE IMAGE'){
            steps{
                script{
                    dockerImage = docker.build(imagename + ":$BUILD_NUMBER", ".")
                }
                
            }
        }

        stage("UPLOAD THE IMAGE"){
            steps{
                script {
                    docker.withRegistry(registryurl,registrycredential){
                        dockerImage.push("$BUILD_NUMBER")
                        dockerImage.push('latest')
                    }
                }
            }
        }


        stage('REMOVE THE CONTAINER IMAGE'){
            steps{
                sh 'docker rmi -f $(docker images -a -q)'
            }
        }


        stage('Deploy to ecs'){
            steps {
                withAws(credentials: 'awscreds',region: 'us-east-1'){
                    sh 'aws ecs update-service --cluster ${cluster} --service ${service} --force-new-deployment'
                }
            }
        }

    }
}