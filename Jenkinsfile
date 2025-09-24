// Jenkinsfile (in the root of your project)

pipeline {
    // 1. Agent: Defines where the pipeline will run. 'any' means any available Jenkins agent.
    agent any

    // 2. Environment: Sets environment variables for the entire pipeline.
    environment {
        // We'll create an ECR repository with this name in AWS.
        ECR_REPO_NAME = "ai-quiz-backend"
        // Replace with your AWS Account ID and Region.
        AWS_ACCOUNT_ID = "044918704633"
        AWS_REGION = "us-east-1" // e.g., us-east-1, eu-central-1
        // The full URI of our ECR repository.
        ECR_REGISTRY = "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"
    }

    // 3. Stages: The main body of the pipeline, broken into logical steps.
    stages {
        // STAGE 1: Check out the code from GitHub (this is handled implicitly by Jenkins but good to know)
        stage('Checkout') {
            steps {
                echo 'Checking out the code...'
                // This step is automatically performed when Jenkins checks out the repository
            }
        }

        // STAGE 2: Build the Docker image for our backend application
        stage('Build Docker Image') {
            steps {
                script {
                    echo "Building the Docker image for the backend..."
                    // We change into the backend directory before running the build command.
                    // The image is tagged with the ECR registry URL and the Jenkins build number.
                    // Using BUILD_NUMBER ensures each image has a unique tag.
                    sh "docker build -t ${ECR_REGISTRY}/${ECR_REPO_NAME}:${BUILD_NUMBER} ./backend"
                }
            }
        }
        
        // STAGE 3: Push the built image to AWS ECR
        stage('Push to AWS ECR') {
            steps {
                script {
                    echo "Logging in to AWS ECR..."
                    // This is the most complex part. We are using the 'withCredentials' block.
                    // Jenkins will securely inject the AWS credentials (which we'll set up in the UI)
                    // into the AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables.
                    // **NEVER PUT SECRET KEYS DIRECTLY IN YOUR JENKINSFILE!**
                    withCredentials([aws(credentialsId: 'aws-credentials', accessKeyVariable: 'AWS_ACCESS_KEY_ID', secretKeyVariable: 'AWS_SECRET_ACCESS_KEY')]) {
                        
                        // This command gets a temporary password from AWS ECR and uses it to log Docker in.
                        sh "aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${ECR_REGISTRY}"
                        
                        echo "Pushing image to ECR..."
                        // Push the image we built in the previous stage.
                        sh "docker push ${ECR_REGISTRY}/${ECR_REPO_NAME}:${BUILD_NUMBER}"
                        
                        echo "Image pushed successfully!"
                    }
                }
            }
        }
    }
    
    // 4. Post-build Actions: These steps run after all stages are complete.
    post {
        always {
            // This is a good practice for cleaning up to prevent old images from filling up disk space.
            echo 'Cleaning up old Docker images...'
            // We'll leave this empty for now, but you could add cleanup commands here.
        }
    }
}
