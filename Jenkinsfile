#!/usr/bin/env groovy
// Scripted Pipeline

// https://jenkins.io/doc/book/pipeline/syntax/#available-options
properties([
  disableConcurrentBuilds()
])

def getBranch(){
  String branch = env.BRANCH_NAME
  if (!branch){
      try {
          branch = sh(script: 'git symbolic-ref --short HEAD', returnStdout: true).toString().trim()
      } catch (err){
          echo('Unable to get git branch and in a detached HEAD. You may need to select Pipeline additional behaviour and \'Check out to specific local branch\'')
          return null
      }
  }
  return branch
}

String getRepoName() {
  return scm.getUserRemoteConfigs()[0].getUrl().tokenize('/')[3].split("\\.")[0]
}

def prepareVenv(String name) {
  sh """
    virtualenv ${name}
    . ${name}/bin/activate
    pip install -r test-requirements.txt
  """
}

def venv(String venv, String cmd, Boolean returnStdout = false) {
  def installed = fileExists("${venv}/bin/activate")

  if(!installed) {
    prepareVenv(venv)
  }

  sh(script: """
    . ${venv}/bin/activate
    ${cmd}
  """, returnStdout: returnStdout)
}

def getPipelineConfig() {
    def settings = [:]
    dir(getRepoName()) {
        settings = readYaml(file: '.jenkins/pipeline.yml')
    }
    return settings
}

def configurePipeline(){
  switch(getBranch()){
    case 'master':
      properties([
        buildDiscarder(logRotator(numToKeepStr: '100')),
        pipelineTriggers([
            pollSCM('H/15 * * * *'),
            cron('@daily')
        ])
      ])
      break
    case 'develop':
      properties([
        buildDiscarder(logRotator(numToKeepStr: '20')),
        pipelineTriggers([pollSCM('H/15 * * * *')])
      ])
      break
    default:
      properties([
        buildDiscarder(logRotator(numToKeepStr: '5')),
        pipelineTriggers([pollSCM('H/15 * * * *')])
      ])
  }
}


def pipelineConfig
try {
  stage('Prepare') {
    node('ansible') {
      // configure cleanup after running pipeline
      cleanWs()
      // ensure we start at a clean workspace state
      deleteDir()
      // checkout project git repository to sub directory
      checkout([
        $class: 'GitSCM',
        branches: scm.branches,
        doGenerateSubmoduleConfigurations: scm.doGenerateSubmoduleConfigurations,
        extensions: scm.extensions << [$class: 'RelativeTargetDirectory', relativeTargetDir: getRepoName()],
        userRemoteConfigs: scm.userRemoteConfigs
      ])
      // stash sourcecode
      stash(includes: getRepoName() + '/**/*', name: 'sourcecode')

      // configure branch specific pipeline
      configurePipeline()

      pipelineConfig = getPipelineConfig()
    }
  }
  stage('Test') {
    stages = [failFast: true]
    for (int i = 0; i < pipelineConfig.tox_envs.size(); i++) {
      def toxEnv = pipelineConfig.tox_envs[i]
      for (int j = 0; j < pipelineConfig.molecule_scenarios.size(); j++) {
        def scenario = pipelineConfig.molecule_scenarios[j]
        stages["${toxEnv}-${scenario}"] = runMoleculeTests(toxEnv, scenario)
      }
    }
    parallel stages
  }
} catch (e) {
  currentBuild.result = 'FAILURE'
  throw e
}

def runMoleculeTests(toxEnv, scenario) {
  return {
    node('ansible') {
      // cleanup workspace on our node
      deleteDir()
      unstash('sourcecode')

      try {
        dir(getRepoName()) {
          sh "mkdir -p ./reports/${toxEnv}-${scenario}"
          withEnv(['PATH+EXTRA=/snap/bin:/var/lib/snapd/snap/bin']) {
            venv('.venv', "tox --parallel--safe-build -e ${toxEnv} -- molecule test -s ${scenario}")
          }
        }
      } catch(e){
        throw e
      } finally {
        try {
          dir(getRepoName()) {
            venv('.venv', "tox --parallel--safe-build -e ${toxEnv} -- ara generate html ./reports/${toxEnv}-${scenario}/html")
          }
          publishHTML(target: [
            reportName: "ARA-${toxEnv}-${scenario}",
            reportDir: getRepoName() + "/reports/${toxEnv}-${scenario}/html",
            reportFiles: 'index.html',
            keepAll: true
          ])
        } catch(e) {
        }
      }
    }
  }
}
