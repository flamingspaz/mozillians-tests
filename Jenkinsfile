/** Desired capabilities */
def capabilities = [
  browserName: 'Firefox',
  version: '57.0',
  platform: 'Windows 10'
]

pipeline {
  agent agent {label 'mesos-testing'}
  libraries {
    lib('fxtest@1.9')
  }
  options {
    ansiColor('xterm')
    timestamps()
    timeout(time: 1, unit: 'HOURS')
  }
  stages {
    stage('Lint') {
      agent {
        dockerfile true
      }
      steps {
        sh "flake8"
      }
    }
    stage('Test') {
      agent {
        dockerfile true
      }
      environment {
        VARIABLES = credentials('MOZILLIANS_VARIABLES')
        PYTEST_PROCESSES = "${PYTEST_PROCESSES ?: "auto"}"
        PULSE = credentials('PULSE')
        SAUCELABS = credentials('SAUCELABS')
      }
      steps {
        writeCapabilities(capabilities, 'capabilities.json')
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
      post {
        always {
          stash includes: 'results/*', name: 'results'
          archiveArtifacts 'results/*'
          junit 'results/*.xml'
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
  }
}