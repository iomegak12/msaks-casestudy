pipeline {
  agent any
  stages {
    stage('Build Calculation Service') {
      parallel {
        stage('Build Calculation Service Image') {
          agent any
          steps {
            dir(path: 'source/calculation-offer-service-v2/CalculationServiceAPISolution') {
              sh '''pwd



'''
              sh 'echo Current Image Name : $CALCULATION_SERVICE_IMAGE $BUILD_NUMBER'
              sh 'docker build -t $CALCULATION_SERVICE_IMAGE .'
              sh 'docker tag $CALCULATION_SERVICE_IMAGE:latest $ACR_ID/$CALCULATION_SERVICE_IMAGE:latest'
            }

          }
        }

        stage('Prune Images') {
          steps {
            sh 'docker image prune -f'
          }
        }

        stage('ECR Login') {
          steps {
            sh 'aws ecr get-login-password --region $REGION | docker login --username AWS --password-stdin $ACR_ID'
          }
        }

        stage('Push Image') {
          steps {
            sh 'docker push $ACR_ID/$CALCULATION_SERVICE_IMAGE:latest'
          }
        }

      }
    }

  }
  environment {
    CALCULATION_SERVICE_IMAGE = 'ramkumar-casestudy-calculation-service'
    ACR_ID = '854669732775.dkr.ecr.ap-south-1.amazonaws.com'
    REGION = 'ap-south-1'
  }
}