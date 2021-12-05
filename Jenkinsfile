pipeline {
  agent any
  stages {
    stage('Build Calculation Service') {
      agent any
      environment {
        CALCULATION_SERVICE_IMAGE = 'ramkumar-casestudy-calculation-service'
        ACD_ID = '854669732775.dkr.ecr.ap-south-1.amazonaws.com'
      }
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

  }
}