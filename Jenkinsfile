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
      docker { 
          image 'python:3.8-slim' 
          label 'agent01'
      }
  }
  stages{
    stage('Install Dependency') {
      steps {
          sh """#!/bin/bash
              python3 -m venv .venv                
              
              . .venv/bin/activate
              
              pip3 install databricks-cli
              
            """
          }
    }
    stage('Setup') {
      steps{
          withCredentials([string(credentialsId: DBTOKEN, variable: 'TOKEN')]) {
            sh """#!/bin/bash
                # Configure Databricks CLI for deployment             
                . .venv/bin/activate

                export DATABRICKS_CONFIG_FILE=./.databrickscfg
                
                
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

            python3 -m venv .venv                
                
            . .venv/bin/activate
            
            export DATABRICKS_CONFIG_FILE=./.databrickscfg
        
            # Use Databricks CLI to deploy notebooks
            STATUS=\$(databricks workspace import_dir -o ${NOTEBOOKPATH} ${WORKSPACEPATH})
            
            if [[ \$STATUS == *"error_code"* ]]; then
                echo \$STATUS
                exit -1
            else
                echo \$STATUS
            fi

            databricks workspace list ${WORKSPACEPATH}
        """
      }
    }
    
  }
}
