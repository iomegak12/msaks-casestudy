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

        stage('Login, Push and Logout') {
          steps {
            sh 'docker login --username $REGISTRY_CREDENTIALS_USR --password $REGISTRY_CREDENTIALS_PSW $ACR_ID'
            sh 'docker push $ACR_ID/$CALCULATION_SERVICE_IMAGE:latest'
            sh 'docker logout'
          }
        }

      }
    }

  }
  environment {
    CALCULATION_SERVICE_IMAGE = 'ramkumar-casestudy-calculation-service'
    ACR_ID = '854669732775.dkr.ecr.ap-south-1.amazonaws.com'
    REGION = 'ap-south-1'
    REGISTRY_CREDENTIALS = credentials('ecr-credentials')
  }
}
