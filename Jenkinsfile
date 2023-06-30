def GITREPO         = "/home/jenkins/workspace/${env.JOB_NAME}"
def GITREPOREMOTE   = "https://github.com/andyhemsft/databricks-demo.git"
def GITHUBCREDID    = "github-access-token"
def CURRENTRELEASE  = "main"
def DBTOKEN         = "databricks-access-token"
def DBURL           = "https://adb-3520826253183044.4.azuredatabricks.net"
def NOTEBOOKPATH    = "${GITREPO}/notebooks"
def BUILDPATH       = "${GITREPO}/Builds/${env.JOB_NAME}-${env.BUILD_NUMBER}"
def WORKSPACEPATH   = "/UAT/Jenkins-Demo"
def DBFSPATH        = "dbfs:<dbfs-path>"
def CLUSTERID       = "<cluster-id>"


pipeline{
  agent {
    node {
        label 'agent01'
    }
  }
  stages{
    stage('Setup') {
      steps{
          withCredentials([string(credentialsId: DBTOKEN, variable: 'TOKEN')]) {
            sh """#!/bin/bash
                # Configure Databricks CLI for deployment

                export PATH=$PATH:$HOME/.local/bin
                
                echo "${DBURL}
                $TOKEN" | databricks configure --token
                
                databricks workspace list
              """
          }
        }
      }
    
    stage('Checkout') { // for display purposes
      steps{
        echo "Pulling ${CURRENTRELEASE} Branch from Github"
        git branch: CURRENTRELEASE, credentialsId: GITHUBCREDID, url: GITREPOREMOTE
      }
    }
    
    stage('Deploy') {
      steps{
        sh """#!/bin/bash
            export PATH=$PATH:$HOME/.local/bin
        
            # Use Databricks CLI to deploy notebooks
            databricks workspace import_dir ${NOTEBOOKPATH} ${WORKSPACEPATH} || exit 0

            databricks workspace list ${WORKSPACEPATH}
        """
      }
    }
    
  }
}