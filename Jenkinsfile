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
            sh 'docker login --username AWS --password $ACR_PASSWORD $ACR_ID'
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
    ACR_PASSWORD = 'eyJwYXlsb2FkIjoicVBXUjl4YS9iMjlEOXdKKzZ0T3luR3RjV2pUSEJlNnBSMU5TTUMxK0trK2YvaVdZRzJsSzJjRnZCYUY4eXBrQnNKQ0J5Y0VlR1RxT3UrdElSQ0ZHTEJOeXEwYWh2ZWlPbHVLZktiMiswY2pwUWRVZGdSWHY3VExGWUhSU3h6V0RSZkdzMnBEZ21OQ1FRcC92Q3BIdlplUmVJZ0NxZUptSXduTkdxaGZiTkF6dGQxaGpGaFdhZzA2OVF1Snh3L01ySy9rSExvRTljY1Z3NWFjYlVESjBNVXc4ZGpRb25UU0VYd3NSQ0Z5aFJpQ1FKaUhvU2ZnWTZ3NmFMRGZpVFpXR1BKcWwwUUMrRjN6c2FHelBWVVRwQXE1cDBZRzR6WDNkT05jYlVBdUhaeTBlN0h5Q1lHMmFIVzBqRVNsV3BBbDR5ajEwSkZSZ0p6MTkwdzFsY1VodG1QTWhRdTMyRXEyMkFRT2xlelFzNEJvWWNMUlVRWW5YeWhUL0hoODVCQ0RLZW1wZWMycFFxSGpnbUliRDM5dHRscWxKYWE4STJsSDZTbWhZZnk2ZzYzSEdyUjNYeElBZW0wNy9MWUxuNW4ydFJyV0I4Rm84Tk1KR3VKTlVDUWQ3NFJvV0ZkTzlnbFFLTlM2U2R0bFhhTTREaHVCNUVUWGorSGdDNHFCL1dLYnpzbWxNSzdGSTFHYkwraEV3WkpQSC9oRHZUNUdYTW5PQTV2dXh1RDVHb2pkQ2Irbmt1NmFCdVZBcm0zUGVYTDF2d3FMcjZ6Z01ycllscWR5OHdiQUdsNE5welZ4ekhkblVOSk1MNU9wamZMVkVPVllLWmxud0tvNjFYZk9zd29OSTRYTUVmeGRPWHh1c0dQTG9maTJMY2t3VUgxYTJnZ0x6V2c5ckgzN1JuQU5zd2xvWUlZQm9md0w5UXk2ZUJwZlVZeEVjN2o4T3ZTOHVVdlJkZEVscElXYWFMZktJWTBkT2NQakovRzAxbWRBZ1pRNUE3VmI1U1BVM09KSmtvRzNKc0dLQzFvSHJOam1tWUJDZUpleTZlZWx2Qk5vRVJpM1FxN1IvNDg2QzlWMEFkRklveFZCT213bEhDTTNwVm4zaFd6dXI5Qzh3QVZ1ZTllbm93OXlTMXJEb2tCeHJjTVZHdmNQRTE5ZEtpTmlmZWFRUDdJR3E5YXhPQndNZGRkSS9zZUNkWnRZS3lLd1N3M3NMWlFrT2pUTGhlZWNreXYwcWxnZ0VudDZ5YlRVbTRsWVpjV3Q5UnhEYXJpcDlrcW5CNTlIQ1dWWHhUbVVhdWxabG82REdwaDBpS2tTdTB2V0kyYzh0cFh6Y0UzdWJQZytjS3ZQL2ZqN3lSS0szcUJQRm9wamVkV3BkQVk1NU51Y1ErajVXU0xjV1hVMkQzaVNzdHFkTkJXQT0iLCJkYXRha2V5IjoiQVFJQkFIaUhXYVlUblJVV0NibnorN0x2TUcrQVB2VEh6SGxCVVE5RnFFbVYyNkJkd3dHWUNQeUlqZWFKRU1hUHJGenh1VHltQUFBQWZqQjhCZ2txaGtpRzl3MEJCd2FnYnpCdEFnRUFNR2dHQ1NxR1NJYjNEUUVIQVRBZUJnbGdoa2dCWlFNRUFTNHdFUVFNWjZBbmtzZWxoYlFObm9QOUFnRVFnRHZOMzAvNThKZjg0TVJUQk1CSXdBeGNJWXFHWUN5WndvRGpyc0RzU3VGOXJhR3BDV2tPNEI3aFRuYnFVZ2xwbmoxTDZMVW1PZjcvaDdCd3lBPT0iLCJ2ZXJzaW9uIjoiMiIsInR5cGUiOiJEQVRBX0tFWSIsImV4cGlyYXRpb24iOjE2Mzg3NTU5ODh9'
  }
}