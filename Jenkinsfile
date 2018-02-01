/** Desired capabilities */
def capabilities = [
  browserName: 'Firefox',
  version: '57.0',
  platform: 'Windows 10'
]
def testImage
pipeline {
  agent {
        node {
            label 'mesos-testing'
        }
    }
  libraries {
    lib('fxtest@1.10')
  }
  options {
    ansiColor('xterm')
    timestamps()
    timeout(time: 1, unit: 'HOURS')
  }
  stages {
    stage('Prep') {
        steps {
            script {testImage = docker.build("mozillians-tests:${env.BUILD_ID}")}
        }
    }
    stage('Lint') {
      steps {
        script{          testImage.inside {
                    sh "flake8"
                }}
      }
    }
    stage('Test') {
      steps {
    script{sh "echo yes"}
/*
        writeCapabilities(capabilities, 'capabilities.json')
        testImage.insde('-e VARIABLES=' + credentials('MOZILLIANS_VARIABLES') + " -e PYTEST_PROCESSES=${PYTEST_PROCESSES ?: "auto"}" + '-e PULSE=' + credentials('PULSE') + ' -e SAUCELABS=' + credentials('SAUCELABS')) {
            sh "pytest " +
              "-n=${PYTEST_PROCESSES} " +
              "--tb=short " +
              "--color=yes " +
              "--driver=SauceLabs " +
              "--variables=capabilities.json " +
              "--variables=${VARIABLES} " +
              "--junit-xml=results/junit.xml " +
              "--html=results/index.html " +
              "--self-contained-html " +
              "--log-raw=results/raw.txt " +
              "--log-tbpl=results/tbpl.txt"
            }
*/
      }
      post {
        always {
          stash includes: 'results/*', name: 'results'
          archiveArtifacts 'results/*'
          junit 'results/*.xml'
          submitToActiveData('results/raw.txt')
          submitToTreeherder('mozillians-tests', 'e2e', 'End-to-end integration tests', 'results/*', 'results/tbpl.txt')
        }
      }
    }
  }
  post {
    always {
      unstash 'results'
      publishHTML(target: [
        allowMissing: false,
        alwaysLinkToLastBuild: true,
        keepAll: true,
        reportDir: 'results',
        reportFiles: 'index.html',
        reportName: 'HTML Report'])
    }
    changed {
      ircNotification()
    }
    failure {
      emailext(
        attachLog: true,
        attachmentsPattern: 'results/index.html',
        body: '$BUILD_URL\n\n$FAILED_TESTS',
        replyTo: '$DEFAULT_REPLYTO',
        subject: '$DEFAULT_SUBJECT',
        to: '$DEFAULT_RECIPIENTS')
    }
  }
}
