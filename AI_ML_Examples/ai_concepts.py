"""
Introduction to AI Concepts
Demonstrates: Basic AI concepts, neural networks, deep learning basics
"""

import numpy as np
import pandas as pd
from sklearn.neural_network import MLPClassifier, MLPRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, mean_squared_error
import warnings
warnings.filterwarnings('ignore')

class AIConceptsDemo:
    """
    Demonstrate fundamental AI and neural network concepts
    """
    
    def __init__(self):
        self.data = None
    
    def neural_network_basics(self):
        """
        Demonstrate basic neural network concepts
        """
        print("=" * 60)
        print("NEURAL NETWORK BASICS")
        print("=" * 60)
        
        print("\n🧠 What is a Neural Network?")
        print("-" * 40)
        print("A neural network is a computational model inspired by the human brain.")
        print("It consists of layers of interconnected nodes (neurons).")
        print("\nKey Components:")
        print("  1. Input Layer - Receives input data")
        print("  2. Hidden Layers - Process information")
        print("  3. Output Layer - Produces predictions")
        print("  4. Weights - Connection strengths between neurons")
        print("  5. Activation Functions - Introduce non-linearity")
        
        print("\n📚 Common Activation Functions:")
        print("  • ReLU (Rectified Linear Unit): max(0, x)")
        print("  • Sigmoid: 1 / (1 + e^(-x))")
        print("  • Tanh: (e^x - e^(-x)) / (e^x + e^(-x))")
        
        # Create simple dataset
        np.random.seed(42)
        X = np.random.randn(1000, 5)  # 1000 samples, 5 features
        y = (X[:, 0] + X[:, 1] - X[:, 2] + np.random.randn(1000) * 0.1 > 0).astype(int)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Scale data
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        print("\n🔧 Building a Neural Network:")
        print("-" * 40)
        
        # Create neural network with different architectures
        architectures = [
            (10,),                    # 1 hidden layer with 10 neurons
            (20, 10),                 # 2 hidden layers
            (50, 25, 10),             # 3 hidden layers
        ]
        
        for i, hidden_layers in enumerate(architectures, 1):
            print(f"\nArchitecture {i}: Input -> {' -> '.join(map(str, hidden_layers))} -> Output")
            
            mlp = MLPClassifier(
                hidden_layer_sizes=hidden_layers,
                activation='relu',
                solver='adam',
                max_iter=1000,
                random_state=42,
                verbose=False
            )
            
            # Train
            mlp.fit(X_train_scaled, y_train)
            
            # Evaluate
            train_accuracy = mlp.score(X_train_scaled, y_train)
            test_accuracy = mlp.score(X_test_scaled, y_test)
            
            print(f"  Training Accuracy: {train_accuracy:.4f}")
            print(f"  Testing Accuracy: {test_accuracy:.4f}")
            print(f"  Number of iterations: {mlp.n_iter_}")
    
    def explain_ai_concepts(self):
        """
        Explain key AI/ML concepts
        """
        print("\n" + "=" * 60)
        print("KEY AI & MACHINE LEARNING CONCEPTS")
        print("=" * 60)
        
        concepts = {
            "🤖 Artificial Intelligence (AI)": """
            The simulation of human intelligence in machines.
            Includes: Learning, Reasoning, Problem-solving, Perception
            Examples: Virtual assistants, Self-driving cars, Image recognition
            """,
            
            "📊 Machine Learning (ML)": """
            A subset of AI where systems learn from data without explicit programming.
            Types:
              • Supervised Learning - Learning from labeled data
              • Unsupervised Learning - Finding patterns in unlabeled data
              • Reinforcement Learning - Learning through trial and error
            """,
            
            "🧠 Deep Learning": """
            A subset of ML using neural networks with multiple layers.
            Applications:
              • Image recognition and computer vision
              • Natural language processing
              • Speech recognition
              • Game playing (AlphaGo, Chess AI)
            """,
            
            "📈 Supervised Learning": """
            Learning from labeled examples (input-output pairs).
            Tasks:
              • Classification - Predicting categories (spam/not spam)
              • Regression - Predicting continuous values (house prices)
            Common Algorithms:
              • Linear Regression, Logistic Regression
              • Decision Trees, Random Forests
              • Support Vector Machines (SVM)
              • Neural Networks
            """,
            
            "🔍 Unsupervised Learning": """
            Finding patterns in unlabeled data.
            Tasks:
              • Clustering - Grouping similar items (customer segmentation)
              • Dimensionality Reduction - Reducing features (PCA)
              • Anomaly Detection - Finding outliers (fraud detection)
            Common Algorithms:
              • K-Means, DBSCAN (clustering)
              • PCA, t-SNE (dimensionality reduction)
              • Autoencoders (neural networks)
            """,
            
            "⚙️ Feature Engineering": """
            Creating and selecting the best features for ML models.
            Techniques:
              • Normalization/Standardization
              • One-hot encoding for categorical variables
              • Creating interaction features
              • Polynomial features
              • Feature selection
            """,
            
            "📉 Overfitting vs Underfitting": """
            Overfitting: Model too complex, memorizes training data
              • High training accuracy, low test accuracy
              • Solutions: Regularization, more data, simpler model
            
            Underfitting: Model too simple, can't capture patterns
              • Low training and test accuracy
              • Solutions: More complex model, better features
            """,
            
            "🎯 Model Evaluation": """
            Metrics for Classification:
              • Accuracy - Overall correctness
              • Precision - Correct positive predictions
              • Recall - Finding all positive cases
              • F1-Score - Balance of precision and recall
              • ROC-AUC - Overall performance
            
            Metrics for Regression:
              • MSE - Mean Squared Error
              • RMSE - Root Mean Squared Error
              • R² - Variance explained by model
              • MAE - Mean Absolute Error
            """,
            
            "🔄 Cross-Validation": """
            Technique to assess model performance reliably.
            Common method: K-Fold Cross-Validation
              • Split data into K folds
              • Train on K-1 folds, test on 1 fold
              • Repeat K times
              • Average the results
            Benefits: Better estimate of model performance
            """,
            
            "🚀 Common AI Applications": """
            • Natural Language Processing (NLP)
              - Chatbots, Translation, Sentiment Analysis
            
            • Computer Vision
              - Face Recognition, Object Detection, Medical Imaging
            
            • Recommender Systems
              - Netflix, Amazon, Spotify recommendations
            
            • Time Series Forecasting
              - Stock prices, Weather prediction, Sales forecasting
            
            • Anomaly Detection
              - Fraud detection, Network intrusion, Quality control
            """
        }
        
        for concept, explanation in concepts.items():
            print(f"\n{concept}")
            print("-" * 60)
            print(explanation.strip())
    
    def emerging_ai_technologies(self):
        """
        Overview of emerging AI technologies
        """
        print("\n" + "=" * 60)
        print("EMERGING AI TECHNOLOGIES")
        print("=" * 60)
        
        technologies = {
            "🗣️ Large Language Models (LLMs)": """
            Examples: GPT-4, Claude, Gemini, LLaMA
            Capabilities:
              • Text generation and completion
              • Question answering
              • Code generation
              • Translation and summarization
              • Reasoning and problem-solving
            """,
            
            "🎨 Generative AI": """
            Creating new content based on learned patterns.
            Types:
              • Text Generation (GPT, Claude)
              • Image Generation (DALL-E, Stable Diffusion, Midjourney)
              • Code Generation (GitHub Copilot, CodeWhisperer)
              • Music and Audio Generation
            Applications: Content creation, Design, Software development
            """,
            
            "🤝 Transformer Architecture": """
            Revolutionary neural network architecture.
            Key Innovation: Attention Mechanism
              • Processes entire sequences at once
              • Understands context and relationships
              • Enables parallel processing
            Impact: Powers modern NLP and vision models
            Examples: BERT, GPT, Vision Transformers
            """,
            
            "🔮 AI in Business Intelligence": """
            Applications:
              • Predictive Analytics - Forecasting trends
              • Customer Segmentation - Targeted marketing
              • Sentiment Analysis - Understanding feedback
              • Automated Reporting - Generating insights
              • Anomaly Detection - Identifying issues
            Tools: Power BI with AI, Tableau, Azure ML
            """,
            
            "☁️ AI on Cloud Platforms": """
            Azure AI Services:
              • Azure Machine Learning
              • Cognitive Services (Vision, Speech, Language)
              • Azure OpenAI Service
            
            AWS AI Services:
              • SageMaker
              • Rekognition, Comprehend, Polly
              • Bedrock (Generative AI)
            
            Google Cloud AI:
              • Vertex AI
              • Cloud Vision, Speech, Translation
            """,
            
            "⚖️ Responsible AI & Ethics": """
            Key Principles:
              • Fairness - Avoiding bias and discrimination
              • Transparency - Explainable AI decisions
              • Privacy - Protecting user data
              • Accountability - Clear responsibility
              • Safety - Preventing harm
            
            Challenges:
              • Bias in training data
              • Privacy concerns
              • Job displacement
              • Deepfakes and misinformation
              • AI alignment and control
            """
        }
        
        for tech, description in technologies.items():
            print(f"\n{tech}")
            print("-" * 60)
            print(description.strip())

def main():
    """Main demonstration function"""
    print("\n" + "=" * 60)
    print("INTRODUCTION TO AI & MACHINE LEARNING CONCEPTS")
    print("=" * 60)
    
    demo = AIConceptsDemo()
    
    # Demonstrate neural networks
    demo.neural_network_basics()
    
    # Explain core concepts
    demo.explain_ai_concepts()
    
    # Emerging technologies
    demo.emerging_ai_technologies()
    
    print("\n" + "=" * 60)
    print("LEARNING RESOURCES")
    print("=" * 60)
    print("""
    📚 Recommended Learning Path:
    
    1. Foundational Math
       • Linear Algebra, Calculus, Statistics
    
    2. Programming
       • Python (NumPy, Pandas, Scikit-learn)
       • Data manipulation and visualization
    
    3. Classical ML
       • Supervised and Unsupervised Learning
       • Model evaluation and tuning
    
    4. Deep Learning
       • Neural Networks, CNNs, RNNs
       • TensorFlow, PyTorch
    
    5. Specialized Topics
       • NLP, Computer Vision, Reinforcement Learning
    
    6. Practical Projects
       • Kaggle competitions
       • Real-world datasets
       • Portfolio projects
    
    📖 Resources:
    • Coursera: Machine Learning by Andrew Ng
    • Fast.ai: Practical Deep Learning
    • Kaggle: Datasets and competitions
    • Papers with Code: Latest research
    • Microsoft Learn: Azure AI fundamentals
    """)
    
    print("\n" + "=" * 60)
    print("✓ AI Concepts demonstration completed!")
    print("=" * 60)

if __name__ == "__main__":
    main()
