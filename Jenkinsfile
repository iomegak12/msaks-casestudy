pipeline {
  agent any
  stages {
    stage('Build Image') {
      agent any
      environment {
        CALCULATION_SERVICE_IMAGE = 'ramkumar-casestudy-calculation-service'
      }
      steps {
        dir(path: 'source/calculation-offer-service-v2/CalculationServiceAPISolution') {
          sh '''pwd



'''
          sh 'echo "Current Image Name : " + $CALCULATION_SERVICE_IMAGE'
        }

      }
    }

  }
}