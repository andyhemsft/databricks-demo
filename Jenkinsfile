def GITREPO         = "workspace/${env.JOB_NAME}"
def GITREPOREMOTE   = "https://github.com/andyhemsft/databricks-demo.git"
def GITHUBCREDID    = "github-access-token"
def CURRENTRELEASE  = "main"
def DBTOKEN         = "databricks-access-token"
def DBURL           = "https://adb-3520826253183044.4.azuredatabricks.net"
def NOTEBOOKPATH    = "${GITREPO}/Workspace"
def BUILDPATH       = "${GITREPO}/Builds/${env.JOB_NAME}-${env.BUILD_NUMBER}"
def WORKSPACEPATH   = "/Shared/UAT/Jenkins-Demo"
def DBFSPATH        = "dbfs:<dbfs-path>"
def CLUSTERID       = "<cluster-id>"


pipeline{
  agent {
    node {
        label 'agent01'
    }
  }
  stage('Setup') {
        withCredentials([string(credentialsId: DBTOKEN, variable: 'TOKEN')]) {
          sh """#!/bin/bash
              # Configure Databricks CLI for deployment
              echo "${DBURL}
              $TOKEN" | databricks configure --token
            """
        }
    }
    
    stage('Checkout') { // for display purposes
      echo "Pulling ${CURRENTRELEASE} Branch from Github"
      git branch: CURRENTRELEASE, credentialsId: GITHUBCREDID, url: GITREPOREMOTE
    }
    /*
    stage('Build Artifact') {
      sh """mkdir -p ${BUILDPATH}/Workspace
            #Get modified files
            git diff --name-only --diff-filter=AMR HEAD^1 HEAD | xargs -I '{}' cp --parents -r '{}' ${BUILDPATH}

            # Generate artifact
            tar -czvf Builds/latest_build.tar.gz ${BUILDPATH}
        """
      archiveArtifacts artifacts: 'Builds/latest_build.tar.gz'
    }
    stage('Deploy') {
      sh """#!/bin/bash
            # Use Databricks CLI to deploy notebooks
            databricks workspace import_dir ${BUILDPATH}/Workspace ${WORKSPACEPATH}

            # dbfs cp -r ${BUILDPATH}/Libraries/python ${DBFSPATH}
        """
    }
    */
}