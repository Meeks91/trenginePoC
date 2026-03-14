[Home](https://www.tutorialspoint.com/) [Whiteboard](https://www.tutorialspoint.com/whiteboard.htm) [Graphing Calculator](https://www.tutorialspoint.com/online_graphing_calculator.htm) [Online Compilers](https://www.tutorialspoint.com/codingground.htm) [Articles](https://www.tutorialspoint.com/articles/index.php) [Tools](https://www.tutorialspoint.com/online_dev_tools.htm)
# Machine Learning (ML) Tutorial
This **Machine Learning (ML) tutorial** will provide a detailed understanding of the concepts of **machine learning** such as, different types of machine learning algorithms, types, applications, libraries used in ML, and real-life examples.
## What is Machine Learning
**Machine Learning (ML)** is a branch of [Artificial Intelligence (AI)](https://www.tutorialspoint.com/artificial_intelligence/index.htm) that works on algorithm developments and statistical models that allow computers to learn from data and make predictions or decisions without being explicitly programmed.
> This Machine Learning With Python Tutorial is based on the Latest Python 3.14.2 versions.
## Online Editor
We have provided an [Online Python Compiler/Interpreter](https://www.tutorialspoint.com/python/online-python-compiler.php). Which helps you to **Edit** and **Execute** the Python code directly from your browser. You can also execute the Python programs using this.
Try to click the icon to run the following Python code to handle categorical data in machine learning.
```


import pandas as pd

# Creating a sample dataset with a categorical variable
data = {'color': ['red', 'green', 'blue', 'red', 'green']}
df = pd.DataFrame(data)

# Performing one-hot encoding
one_hot_encoded = pd.get_dummies(df['color'], prefix='color')

# Combining the encoded data with the original data
df = pd.concat([df, one_hot_encoded], axis=1)

# Drop the original categorical variable
df = df.drop('color', axis=1)

# Print the encoded data
print(df)


```

## How does Machine Learning Work?
Machine Learning process includes Project Setup, Data Preparation, Modeling and Deployment. The following figure demonstrates the common working process of Machine Learning. It follows some set of steps to do the task; a sequential process of its workflow is as follows:
## Stages of Machine Learning
The following are the stages (detailed sequential process) of Machine Learning:
**Data Collection** − Data collection is an initial step in the process of machine learning. In this stage, it collects data from the different sources such as databases, text files, pictures, sound files, or web scraping. This process organizes the data in an appropriate format, such as a CSV file or database, and makes sure that they are useful for solving your problem.
**Data Pre-processing** − It is a key step in the process of machine learning, which involves deleting duplicate data, fixing errors, managing missing data either by eliminating or filling it in, and adjusting and formatting the data.
**Choosing the Right Model** − The next step is to select a machine learning model; once data is prepared, then we apply it to ML models like linear regression, decision trees, and neural networks that may be selected to implement. This selection depends on many factors, such as the kind of data and your problem, the size and type of data, the complexity, and the computational resources.
**Training the Model** − This step includes training the model from the data so it can make better predictions.
**Evaluating the model** − When module is trained, the model has to be tested on new data that they haven't been able to see during training. 
**Hyperparameter Tuning and Optimization** − After evaluating the model, you may need to adjust its hyperparameters to make it more efficient. You should try different combinations of parameters and cross-validation to ensure that the model performs well on different data sets.
**Predictions and Deployment** − When the model has been programmed and optimized, it will be ready to estimate new data. This is done by adding new data to the model and using its output for decision-making or other analysis. The deployment includes its integration into a production environment to make it capable of processing real-world data.
## Types of Machine Learning
Machine learning models fall into the following categories:
**1.[Supervised Machine Learning](https://www.tutorialspoint.com/machine_learning/machine_learning_supervised.htm)** − It is a type of machine learning that trains the model using labeled datasets to predict outcomes.
**2.[Unsupervised Machine Learning](https://www.tutorialspoint.com/machine_learning/machine_learning_unsupervised.htm)** − It is a type of machine learning that learns patterns and structures within the data without human supervision.
**3.[Semi-supervised Learning](https://www.tutorialspoint.com/machine_learning/machine_learning_semi_supervised_learning.htm)** − It is a type of machine learning that is neither fully supervised nor fully unsupervised. The semi-supervised learning algorithms basically fall between supervised and unsupervised learning methods.
**4.[Reinforcement Machine Learning](https://www.tutorialspoint.com/machine_learning/machine_learning_reinforcement_learning.htm)** − It is a type of machine learning model that is similar to supervised learning but does not use sample data to train the algorithm. This model learns by trial and error.
## Common Machine Learning Algorithms
Several machine learning algorithms are commonly used. These include:
  * **Neural Networks** − It works like the human brain with many connected nodes. They help to find patterns and are used in language processing, image and speech recognition, and creating images.
  * **Linear Regression** − It predicts numbers based on past data. For example, it helps estimate house prices in an area.
  * **Logistic Regression** − It predicts like "yes/no" answers and it is useful for spam detection and quality control.
  * **Clustering** − It is used to group similar data without instructions and it helps to find patterns that humans might miss.
  * **Decision Trees** − They help to classify data and predict numbers using a tree-like structure. They are easy to check and understand.
  * **Random forests** − They combine multiple decision trees to improve predictions.


## Importance of Machine Learning
Machine Learning is important in automation, extracting insights from data, and decision-making processes. It has its significance due to the following reasons:
  * **Data Processing** − Machine learning is useful to analyze large data from social media, sensors, and other sources and help to reveal patterns and insights to improve decision-making.
  * **Data-Driven Insights** − Machine learning algorithms find trends and connections in big data that humans might miss, which helps to take better decisions and predictions.
  * **Automation** − Machine learning automates the repetitive tasks, reducing errors and saving time.
  * **Personalization** − Machine learning is useful to analyze the user preferences to provide personalized recommendations in e-commerce, social media, and streaming services. It helps in many manners, such as to improve user engagement, etc.
  * **Predictive Analytics** − Machine learning models use past data to predict future outcomes, which may help for sales forecasts, risk management, and demand planning.
  * **Pattern Recognition** − Machine learning is useful in pattern recognition during image processing, speech recognition, and natural language processing.
  * **Finance** − Machine learning is used in credit scoring, fraud detection, and algorithmic trading.
  * **Retail** − Machine learning helps to enhance the recommendation systems, supply chain management, and customer service.
  * **Fraud Detection & Cybersecurity** − Machine learning detects the fraudulent transactions and security threats in real time.
  * **Continuous Improvement** − Machine learning models update regularly with new data, which allows them to adapt and improve over time.


## Applications of Machine Learning
Machine learning is used in various fields. Some of the most common applications include:
  * **Speech Recognition** − Machine learning is used to convert spoken language into text using natural language processing (NLP). It is used in voice assistants like Siri, voice search, and text accessibility features on mobile devices.
  * **Customer Service** − There are several chatbots that are useful for reducing human interaction and providing better support on websites and social media, handling FAQs, giving recommendations, and assisting in e-commerce. For example, virtual agents, Facebook Messenger bots, and voice assistants.
  * **Computer Vision** − It helps computers in analyzing the images and videos to take action. It is used in social media for photo tagging, in healthcare for medical imaging, and in self-driving cars for navigation.
  * **Recommendation Engines** − ML recommendation engines suggest products, movies, or content based on user behavior. Online retailers use them to improve shopping experiences.
  * **Robotic Process Automation (RPA)** − RPA uses AI to automate repetitive tasks and reduce manual work.
  * **Automated Stock Trading** − AI-driven trading platforms make rapid trades to optimize stock portfolios without human intervention.
  * **Fraud Detection** − Machine learning identifies suspicious financial transactions, which help banks to detect fraud and prevent unauthorized activities.


## Who can Learn Machine Learning?
This **machine learning tutorial** has been prepared for those who want to learn about the basics and advances of Machine Learning. In a broader sense; ML is a subset of Artificial Intelligence (AI) that focuses on developing algorithms and models that allow computers to learn from data and make predictions or decisions without being explicitly programmed to do so. Machine learning requires data. This data can be text, images, audio, numbers, or video. The quality and quantity of data considerably affect machine learning model performance. Features are data qualities used to predict or decide. Feature selection and engineering entail selecting and formatting the most relevant features for the model.
## Prerequisites to Learn Machine Learning
You should have a basic understanding of the technical aspects of Machine Learning. Learners should be familiar with data, information, and its basics. Knowledge of Data, information, structured data, unstructured data, semi-structured data, data processing, and Artificial Intelligence basics; Proficiency in labeled / unlabelled data, feature extraction from data, and their application in ML to solve common problems is a must.
## Frequently Asked Questions about Machine Learning
There are some very Frequently Asked Questions(FAQ) about Machine Learning. In this section, we will have some of these FAQs answered −
What is Machine Learning?
Machine learning (ML) is a subset of artificial intelligence (AI) that focuses on developing algorithms that improve automatically through experience and by using the hidden patterns of the data.
In simple terms, ML enables computers to learn from data and make predictions or decisions without being explicitly programmed. This capability allows computers to automate tasks and solve complex problems across different fields.
Why is Machine Learning Important?
The amount of data generated by businesses and individuals continues to grow at an exponential rate. Machine learning has become an important topic as it revolutionizes how computers process and interpret data.
ML empowers computers to learn from data, enhancing accuracy and efficiency in various tasks. It enables data-driven decision-making and boosts productivity.
What are the different types of Machine Learning?
Different types of Machine Learning include −
  * **Supervised Learning** − In supervised learning, the algorithm is trained on labeled data i.e., the correct answer or output is provided for each input.
  * **Unsupervised Learning** − In unsupervised learning, the algorithm is trained on unlabeled data i.e., the correct output or answer is not provided for each input.
  * **Reinforcement Learning** − In reinforcement learning, the algorithm learns by receiving feedback in the form of rewards or punishments based on its actions.
  * **Semi-supervised Learning** − In semi-supervised learning, the algorithm is trained on combined labeled and unlabeled data.


What are some common applications of Machine Learning?
Some of the common applications of Machine Learning include −
  * Recommendation systems for personalized content.
  * Image and speech recognition for authentication and security.
  * Natural language processing for sentiment analysis and chatbots.
  * Predictive analytics for forecasting sales and trends.
  * Autonomous vehicles for navigation and decision-making.
  * Fraud detection in the banking sector and finance.
  * Medical diagnosis and healthcare management.
  * Virtual assistants for customer service and support.


What are the basic components of a Machine Learning system?
The basic components of a Machine Learning system −
  * **Data** − It is the raw information used to train and test the model.
  * **Model** − It is a mathematical representation that learns from the input data.
  * **Features** − These are the input variables or attributes used by the model to make predictions.
  * **Training** − Process of feeding data into the model to make accurate predictions by adjusting its internal parameters.
  * **Evaluation** − Process of assessing the performance of model on separate dataset.
  * **Prediction** − Process of using the trained model to make predictions on new data.


What programming languages are commonly used in Machine Learning?
Some of the commonly used programming languages in Machine Learning include Python, R, Java, C++, Julia, and JavaScript. 
Python, due to its simplicity and extensive libraries like TensorFlow, Keras, Scikit-learn, and OpenCV is the preferred choice for both beginners as well as experts in the field of machine learning.
What is the difference between supervised and unsupervised learning?
In supervised learning, an algorithm is trained using the labeled data to find the relationship between the input variables and the desired output. On the other hand, in unsupervised learning, an algorithm is trained using unlabeled data to find the structure and patterns from the input data.
Supervised learning can be used for **classification** and **regression** while unsupervised learning can be used for **clustering and dimensionality reduction**.
What are some popular algorithms used in Machine Learning?
Here is a list of some popular algorithms used in Machine Learning −
  * Linear Regression
  * Logistic Regression
  * Decision Trees
  * Random Forests
  * Support Vector Machines (SVM)
  * k-Nearest Neighbors (k-NN)
  * Naive Bayes
  * Gradient Boosting Machines (GBM)
  * K-Means Clustering
  * Hierarchical Clustering


How do I evaluate the performance of a Machine Learning model?
For classification tasks, we can evaluate the performance of a Machine Learning model using various metrics such as **accuracy, precision, recall, F1-score** , and **area under the ROC curve (AUC-ROC)**.
For regression tasks, we can use metrics like **mean squared error (MSE), root mean squared error (RMSE)** , and **R-squared**. Cross-validation techniques like k-fold cross-validation can also help assessing generalization performance of a ML model.
What are some common challenges in Machine Learning?
Some common challenges and issues faced in Machine Learning include overfitting, underfitting, data quality, imbalanced datasets, computational complexity, model interpretability, generalization, scalability, and ethical considerations like fairness and privacy protection.
How do I get started with Machine Learning?
To get started with ML, first learn Python programming language which is widely used in the field. Understand some ML concepts like supervised and unsupervised learning, algorithms, and evaluation metrics.
To implement ML models, it is good to learn popular libraries like scikit-learn and TensorFlow. You can practice by working on projects using datasets from platforms like Kaggle.
You can also take some online courses to gain practical experience. Finally, build your own ML projects to apply your knowledge.
What are some ethical considerations in Machine Learning?
Machine learning models can raise ethical considerations when used to make decisions affecting people's lives. These considerations include bias and fairness, privacy, transparency, accountability, data security, consent, societal impact, and regulatory compliance.
To ensure a reliable development and deployment of machine learning systems, considering these aspects are important.
What is the difference between Machine Learning and Artificial Intelligence?
Machine Learning (ML) and Artificial Intelligence (AI) are two closely related but different domains withing computer science. AI is a field of computer science that makes computers mimic human intelligence.
On the other hand, ML is a subset of AI that focuses on algorithms that allow computers to learn from data and make predictions or decisions without being explicitly programmed to do so.
Can Machine Learning be applied to any type of data?
Machine Learning can be applied to various types of data such as numerical, categorical, text, image, and audio data. But the effectiveness of Machine Learning techniques depends on the quality and characteristics of the data.
For example, supervised learning algorithms require labeled data for training, while unsupervised learning techniques require unlabeled data.
How do I collect and prepare data for Machine Learning?
To collect and prepare data for Machine Learning, start by defining the problem and gathering relevant data from various sources. Next, clean the dataset by removing duplicates and handling missing values. Now, Analyze the dataset to understand its structure and relationships between variables.
Next, prepare the data for input into ML models by using techniques like normalization and scaling. Now, divide the dataset into training and testing sets for model evaluation. Finally, iterate on the data preparation process based on model performance.
What are some common tools and libraries used in Machine Learning projects?
Some common tools and libraries used in Machine Learning projects include Python programming language (with libraries like **TensorFlow, Scikit-learn, PyTorch, Keras** etc.), R programming language (with libraries like **caret, mlr** , etc.), Jupyter Notebooks, NumPy, Pandas, Matplotlib, Seaborn, and XGBoost.
These tools enable data manipulation, visualization, model development, and evaluation and hence play a fundamental role in ML workflow.
How do I choose the right Machine Learning algorithm for my problem?
To choose the right Machine Learning algorithm, you first need to understand your problem and analyze the characteristics of your data.
For example, if you want to categorize new observations, you may need to use classification techniques, while if you want to analyze relationship between dependent and independent variables, you may need to use regression techniques.
What is deep learning and how does it relate to Machine Learning?
Deep Learning (DL) is a subset of Machine Learning (ML) that uses neural networks with multiple layers to learn hierarchical representations of data. It relates to ML as it falls withing the broader field of ML.
While ML uses various algorithms to teach computers to learn from data, DL focuses on using deep neural networks to learn complex patterns and relationships in large data sets.
How do I train a Machine Learning model?
To train a Machine Learning model, first clean, preprocess and split the data into training and testing sets. Next, choose an appropriate algorithm or model architecture. Now, train it on the training data by adjusting parameters to minimize error. 
Once trained, validate the models performance on a separate dataset, Finally, evaluate the models performance on testing data and deploy the model for predictions on new data.
How can I deploy a Machine Learning model into production?
To deploy a Machine Learning model into production first choose a suitable platform for hosting the model. Next, implement a pipeline for model deployment which includes preprocessing, prediction, and post-processing steps.
Next, we need to validate the deployed model's performance and functionality. Once validated, continuously monitor the model's performance in production. Finally, if needed, scale the deployment to handle increasing workload and demand efficiently.
Print Page 
Advertisements
# tutorialspoint.com asks for your consent to use your personal data to:
  * Personalised advertising and content, advertising and content measurement, audience research and services development
  * Store and/or access information on a device


Learn more
  * [How can I change my choice?](https://www.tutorialspoint.com/machine_learning/index.htm#)
  * [What if I don't consent?](https://www.tutorialspoint.com/machine_learning/index.htm#)
  * [How does legitimate interest work?](https://www.tutorialspoint.com/machine_learning/index.htm#)
  * [Do I have to consent to everything?](https://www.tutorialspoint.com/machine_learning/index.htm#)


Your personal data will be processed and information from your device (cookies, unique identifiers, and other device data) may be stored by, accessed by and shared with 696 partners, or used specifically by this site. We and our partners may use precise geolocation data. [List of partners.](https://www.tutorialspoint.com/machine_learning/index.htm#)
Some vendors may process your personal data on the basis of legitimate interest, which you can object to by managing your options below. Look for a link at the bottom of this page or in the site menu to manage or withdraw consent in privacy and cookie settings.
Consent
Manage options
Data preferences
# Manage your data
You can choose how your personal data is used. Vendors want your permission to do the following:
TCF vendors
## Store and/or access information on a device
Cookies, device or similar online identifiers (e.g. login-based identifiers, randomly assigned identifiers, network based identifiers) together with other information (e.g. browser type and information, language, screen size, supported technologies etc.) can be stored or read on your device to recognise it each time it connects to an app or to a website, for one or several of the purposes presented here.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent (467 vendors)
## Use limited data to select advertising
Advertising presented to you on this service can be based on limited data, such as the website or app you are using, your non-precise location, your device type or which content you are (or have been) interacting with (for example, to limit the number of times an ad is presented to you).
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent (308 vendors)Legitimate interest (123 vendors)
## Create profiles for personalised advertising
Information about your activity on this service (such as forms you submit, content you look at) can be stored and combined with other information about you (for example, information from your previous activity on this service and other websites or apps) or similar users. This is then used to build or improve a profile about you (that might include possible interests and personal aspects). Your profile can be used (also later) to present advertising that appears more relevant based on your possible interests by this and other entities.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent (363 vendors)
## Use profiles to select personalised advertising
Advertising presented to you on this service can be based on your advertising profiles, which can reflect your activity on this service or other websites or apps (like the forms you submit, content you look at), possible interests and personal aspects.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent (367 vendors)
## Create profiles to personalise content
Information about your activity on this service (for instance, forms you submit, non-advertising content you look at) can be stored and combined with other information about you (such as your previous activity on this service or other websites or apps) or similar users. This is then used to build or improve a profile about you (which might for example include possible interests and personal aspects). Your profile can be used (also later) to present content that appears more relevant based on your possible interests, such as by adapting the order in which content is shown to you, so that it is even easier for you to find content that matches your interests.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent (157 vendors)
## Use profiles to select personalised content
Content presented to you on this service can be based on your content personalisation profiles, which can reflect your activity on this or other services (for instance, the forms you submit, content you look at), possible interests and personal aspects. This can for example be used to adapt the order in which content is shown to you, so that it is even easier for you to find (non-advertising) content that matches your interests.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent (138 vendors)
## Measure advertising performance
Information regarding which advertising is presented to you and how you interact with it can be used to determine how well an advert has worked for you or other users and whether the goals of the advertising were reached. For instance, whether you saw an ad, whether you clicked on it, whether it led you to buy a product or visit a website, etc. This is very helpful to understand the relevance of advertising campaigns.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent (316 vendors)Legitimate interest (159 vendors)
## Measure content performance
Information regarding which content is presented to you and how you interact with it can be used to determine whether the (non-advertising) content e.g. reached its intended audience and matched your interests. For instance, whether you read an article, watch a video, listen to a podcast or look at a product description, how long you spent on this service and the web pages you visit etc. This is very helpful to understand the relevance of (non-advertising) content that is shown to you.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent (156 vendors)Legitimate interest (63 vendors)
## Understand audiences through statistics or combinations of data from different sources
Reports can be generated based on the combination of data sets (like user profiles, statistics, market research, analytics data) regarding your interactions and those of other users with advertising or (non-advertising) content to identify common characteristics (for instance, to determine which target audiences are more receptive to an ad campaign or to certain contents).
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent (235 vendors)Legitimate interest (73 vendors)
## Develop and improve services
Information about your activity on this service, such as your interaction with ads or content, can be very helpful to improve products and services and to build new products and services based on user interactions, the type of audience, etc. This specific purpose does not include the development or improvement of user profiles and identifiers.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent (250 vendors)Legitimate interest (133 vendors)
## Use limited data to select content
Content presented to you on this service can be based on limited data, such as the website or app you are using, your non-precise location, your device type, or which content you are (or have been) interacting with (for example, to limit the number of times a video or an article is presented to you).
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent (61 vendors)Legitimate interest (22 vendors)
## Ensure security, prevent and detect fraud, and fix errors
Your data can be used to monitor for and prevent unusual and possibly fraudulent activity (for example, regarding advertising, ad clicks by bots), and ensure systems and processes work properly and securely. It can also be used to correct any problems you, the publisher or the advertiser may encounter in the delivery of content and ads and in your interaction with them.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#)
## Deliver and present advertising and content
Certain information (like an IP address or device capabilities) is used to ensure the technical compatibility of the content or advertising, and to facilitate the transmission of the content or ad to your device.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#)
## Save and communicate privacy choices
The choices you make regarding the purposes and entities listed in this notice are saved and made available to those entities in the form of digital signals (such as a string of characters). This is necessary in order to enable both this service and those entities to respect such choices.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#)
## Match and combine data from other data sources
Information about your activity on this service may be matched and combined with other information relating to you and originating from various sources (for instance your activity on a separate online service, your use of a loyalty card in-store, or your answers to a survey), in support of the purposes explained in this notice.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#)
## Link different devices
In support of the purposes explained in this notice, your device might be considered as likely linked to other devices that belong to you or your household (for instance because you are logged in to the same service on both your phone and your computer, or because you may use the same Internet connection on both devices).
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#)
## Identify devices based on information transmitted automatically
Your device might be distinguished from other devices based on information it automatically sends when accessing the Internet (for instance, the IP address of your Internet connection or the type of browser you are using) in support of the purposes exposed in this notice.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#)
## Use precise geolocation data
With your acceptance, your precise location (within a radius of less than 500 metres) may be used in support of the purposes explained in this notice.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Actively scan device characteristics for identification
With your acceptance, certain characteristics specific to your device might be requested and used to distinguish it from other devices (such as the installed fonts or plugins, the resolution of your screen) in support of the purposes explained in this notice.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
You can choose your data preferences. This site wants your permission to do the following:
Site
## Store and/or access information on a device
Cookies, device or similar online identifiers (e.g. login-based identifiers, randomly assigned identifiers, network based identifiers) together with other information (e.g. browser type and information, language, screen size, supported technologies etc.) can be stored or read on your device to recognise it each time it connects to an app or to a website, for one or several of the purposes presented here.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Use limited data to select advertising
Advertising presented to you on this service can be based on limited data, such as the website or app you are using, your non-precise location, your device type or which content you are (or have been) interacting with (for example, to limit the number of times an ad is presented to you).
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#)
Legitimate interest
## Create profiles for personalised advertising
Information about your activity on this service (such as forms you submit, content you look at) can be stored and combined with other information about you (for example, information from your previous activity on this service and other websites or apps) or similar users. This is then used to build or improve a profile about you (that might include possible interests and personal aspects). Your profile can be used (also later) to present advertising that appears more relevant based on your possible interests by this and other entities.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Use profiles to select personalised advertising
Advertising presented to you on this service can be based on your advertising profiles, which can reflect your activity on this service or other websites or apps (like the forms you submit, content you look at), possible interests and personal aspects.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Create profiles to personalise content
Information about your activity on this service (for instance, forms you submit, non-advertising content you look at) can be stored and combined with other information about you (such as your previous activity on this service or other websites or apps) or similar users. This is then used to build or improve a profile about you (which might for example include possible interests and personal aspects). Your profile can be used (also later) to present content that appears more relevant based on your possible interests, such as by adapting the order in which content is shown to you, so that it is even easier for you to find content that matches your interests.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Use profiles to select personalised content
Content presented to you on this service can be based on your content personalisation profiles, which can reflect your activity on this or other services (for instance, the forms you submit, content you look at), possible interests and personal aspects. This can for example be used to adapt the order in which content is shown to you, so that it is even easier for you to find (non-advertising) content that matches your interests.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Measure advertising performance
Information regarding which advertising is presented to you and how you interact with it can be used to determine how well an advert has worked for you or other users and whether the goals of the advertising were reached. For instance, whether you saw an ad, whether you clicked on it, whether it led you to buy a product or visit a website, etc. This is very helpful to understand the relevance of advertising campaigns.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#)
Legitimate interest
## Measure content performance
Information regarding which content is presented to you and how you interact with it can be used to determine whether the (non-advertising) content e.g. reached its intended audience and matched your interests. For instance, whether you read an article, watch a video, listen to a podcast or look at a product description, how long you spent on this service and the web pages you visit etc. This is very helpful to understand the relevance of (non-advertising) content that is shown to you.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#)
Legitimate interest
## Understand audiences through statistics or combinations of data from different sources
Reports can be generated based on the combination of data sets (like user profiles, statistics, market research, analytics data) regarding your interactions and those of other users with advertising or (non-advertising) content to identify common characteristics (for instance, to determine which target audiences are more receptive to an ad campaign or to certain contents).
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#)
Legitimate interest
## Develop and improve services
Information about your activity on this service, such as your interaction with ads or content, can be very helpful to improve products and services and to build new products and services based on user interactions, the type of audience, etc. This specific purpose does not include the development or improvement of user profiles and identifiers.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#)
Legitimate interest
## Use limited data to select content
Content presented to you on this service can be based on limited data, such as the website or app you are using, your non-precise location, your device type, or which content you are (or have been) interacting with (for example, to limit the number of times a video or an article is presented to you).
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#)
Legitimate interest
How this consent management platform (CMP) works:
CMP privacy choices
## Storage, duration, and usage details
The choices you make with this CMP regarding the purposes and entities will affect how personalized advertising is presented to you. We need to store these choices to respect them on future visits, and they are stored differently based on the type of site or app you're using:
  * For **sites** , your choices are saved in a cookie named “FCCDCF” for a maximum duration of 390 days.
  * For **apps** , your choices are saved in device storage prefixed by “IABTCF_”. Your choices will be invalidated after 390 days and overwritten once you make new privacy choices on this app.
  * For **accelerated mobile page (AMP) sites** , your choices are saved in local storage prefixed by “amp-store”. Your choices will be invalidated after 390 days and overwritten once you make new privacy choices on this site.


Vendor preferences
Accept all
Confirm choices
Vendor preferences
# Confirm our vendors
Vendors can use your data to provide services. Declining a vendor can stop them from using the data you shared.
TCF vendors
## Exponential Interactive, Inc d/b/a VDX.tv
Cookie duration: 90 (days).
Data collected and processed: IP addresses, Device identifiers, Probabilistic identifiers, Browsing and interaction data, Non-precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. 
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Captify Technologies Limited
Cookie duration: 365 (days).
Data collected and processed: IP addresses, Device characteristics, Probabilistic identifiers, Browsing and interaction data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Roq.ad GmbH
Cookie duration: 365 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Authentication-derived identifiers, Browsing and interaction data, Non-precise location data, Precise location data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. 
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Index Exchange Inc. 
Cookie duration: 365 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Non-precise location data, Precise location data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Quantcast
Cookie duration: 1825 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Authentication-derived identifiers, Browsing and interaction data, User-provided data, Non-precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## BeeswaxIO Corporation
Cookie duration: 395 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Browsing and interaction data, Non-precise location data, Precise location data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Sovrn, Inc.
Cookie duration: 365 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Browsing and interaction data, Non-precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Adkernel LLC
Cookie duration: 180 (days).
Data collected and processed: IP addresses, Device identifiers, Non-precise location data, Precise location data, Users’ profiles
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. 
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## Adikteev
Doesn't use cookies.
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Authentication-derived identifiers, Non-precise location data, Users’ profiles
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## RTB House S.A.
Cookie duration: 365 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Browsing and interaction data, Non-precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## N.Rich Technologies Inc.
Cookie duration: 540 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Authentication-derived identifiers, Browsing and interaction data, User-provided data, Non-precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. 
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## The UK Trade Desk Ltd
Cookie duration: 365 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Authentication-derived identifiers, Browsing and interaction data, Non-precise location data, Precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## Nexxen Inc.
Cookie duration: 180 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Browsing and interaction data, Non-precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## Epsilon
Cookie duration: 400 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Authentication-derived identifiers, Browsing and interaction data, User-provided data, Non-precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Yahoo EMEA Limited
Cookie duration: 750 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Authentication-derived identifiers, Browsing and interaction data, Non-precise location data, Precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. 
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## ADventori SAS
Cookie duration: 90 (days).
Data collected and processed: IP addresses, Device identifiers, Probabilistic identifiers, Browsing and interaction data, User-provided data, Non-precise location data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Triple Lift, Inc.
Cookie duration: 90 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Authentication-derived identifiers, Browsing and interaction data, Non-precise location data, Precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## BidTheatre AB
Cookie duration: 90 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Authentication-derived identifiers, Browsing and interaction data, Non-precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. 
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## Ogury Ltd
Cookie duration: 183 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Authentication-derived identifiers, Browsing and interaction data, User-provided data, Non-precise location data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Xandr, Inc.
Cookie duration: 90 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Authentication-derived identifiers, Browsing and interaction data, Non-precise location data, Precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## ShareThis, Inc
Cookie duration: 390 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Browsing and interaction data, Non-precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Nexxen Group LLC
Cookie duration: 365 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Browsing and interaction data, Non-precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. 
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## NEURAL.ONE
Cookie duration: 365 (days).
Data collected and processed: IP addresses, Device characteristics, Probabilistic identifiers, Browsing and interaction data, Non-precise location data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## ADITION (Virtual Minds GmbH)
Cookie duration: 90 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Browsing and interaction data, User-provided data, Non-precise location data, Precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Active Agent (Virtual Minds GmbH)
Cookie duration: 90 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Browsing and interaction data, User-provided data, Non-precise location data, Precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Taboola Europe Limited
Cookie duration: 366 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Browsing and interaction data, Non-precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## Adex (Virtual Minds GmbH)
Cookie duration: 90 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Browsing and interaction data, User-provided data, Non-precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Equativ
Cookie duration: 366 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Authentication-derived identifiers, Browsing and interaction data, Non-precise location data, Precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Skimbit Ltd
Doesn't use cookies.
Data collected and processed: IP addresses, Device characteristics, Browsing and interaction data, Non-precise location data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Legitimate interest
## Adform A/S
Cookie duration: 3650 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Authentication-derived identifiers, Browsing and interaction data, User-provided data, Non-precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## Magnite, Inc. 
Cookie duration: 365 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Browsing and interaction data, Non-precise location data, Precise location data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## Madison Logic, Inc.
Cookie duration: 45 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Browsing and interaction data, User-provided data, Non-precise location data, Precise location data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Confiant Inc.
Doesn't use cookies.
Data collected and processed: Device characteristics, Non-precise location data
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
## RATEGAIN ADARA INC
Cookie duration: 365 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Authentication-derived identifiers, Browsing and interaction data, User-provided data, Non-precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. 
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## 33Across
Cookie duration: 366 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Browsing and interaction data, Non-precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. 
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Sift Media, Inc
Doesn't use cookies.
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Non-precise location data, Precise location data
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Rakuten Marketing LLC
Cookie duration: 730 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Authentication-derived identifiers, Browsing and interaction data, User-provided data, Non-precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## GumGum, Inc.
Cookie duration: 1831 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Browsing and interaction data, Non-precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Justpremium BV
Cookie duration: 365 (days).
Data collected and processed: IP addresses, Device characteristics, Browsing and interaction data, Non-precise location data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. 
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Lumen Research Limited
Doesn't use cookies.
Data collected and processed: IP addresses, Device characteristics, Browsing and interaction data, Non-precise location data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## adsquare GmbH
Doesn't use cookies.
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Authentication-derived identifiers, Browsing and interaction data, User-provided data, Non-precise location data, Precise location data, Users’ profiles
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## OpenX
Cookie duration: 365 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Browsing and interaction data, Non-precise location data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Yieldlab (Virtual Minds GmbH)
Cookie duration: 90 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Browsing and interaction data, User-provided data, Non-precise location data, Precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Nano Interactive Group Ltd.
Doesn't use cookies.
Data collected and processed: Device characteristics, Browsing and interaction data, Non-precise location data
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Simplifi Holdings LLC
Cookie duration: 366 (days).
Data collected and processed: IP addresses, Device identifiers, Precise location data
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## M32 Connect Inc
Cookie duration: 365 (days).
Data collected and processed: IP addresses, Browsing and interaction data, Non-precise location data
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. 
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## PubMatic, Inc
Cookie duration: 1827 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Authentication-derived identifiers, Browsing and interaction data, User-provided data, Non-precise location data, Precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## Comscore B.V.
Cookie duration: 720 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Authentication-derived identifiers, Browsing and interaction data, User-provided data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Flashtalking
Cookie duration: 730 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Authentication-derived identifiers, Browsing and interaction data, Non-precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. 
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Sharethrough, Inc
Cookie duration: 30 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Browsing and interaction data, Non-precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## PulsePoint, Inc.
Cookie duration: 1830 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Smaato, Inc.
Cookie duration: 21 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Authentication-derived identifiers, Browsing and interaction data, User-provided data, Non-precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Crimtan Holdings Limited
Cookie duration: 365 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Authentication-derived identifiers, Browsing and interaction data, User-provided data, Non-precise location data, Precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. 
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## Teroa S.A.
Cookie duration: 2555 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Browsing and interaction data, Non-precise location data
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. 
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Criteo SA
Cookie duration: 390 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Authentication-derived identifiers, Browsing and interaction data, Non-precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Adloox SA
Doesn't use cookies.
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Browsing and interaction data, Non-precise location data
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## Epsilon (Lotame)
Cookie duration: 274 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Authentication-derived identifiers, Browsing and interaction data, User-provided data, Non-precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## LiveRamp
Cookie duration: 3653 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Authentication-derived identifiers, Browsing and interaction data, Non-precise location data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## WPP Media
Cookie duration: 395 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Authentication-derived identifiers, Browsing and interaction data, Non-precise location data, Precise location data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. 
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## Fifty Technology Limited
Cookie duration: 365 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Browsing and interaction data, Non-precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. 
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Sonobi, Inc
Cookie duration: 365 (days).
Data collected and processed: IP addresses, Device identifiers, Non-precise location data
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. 
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## Rich Audience Technologies SLU
Cookie duration: 365 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Non-precise location data
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. 
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## LoopMe Limited
Cookie duration: 90 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Browsing and interaction data, User-provided data, Non-precise location data, Precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Dynata LLC
Cookie duration: 365 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Authentication-derived identifiers, Browsing and interaction data, User-provided data, Non-precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. 
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Showheroes SE
Cookie duration: 393 (days).
Data collected and processed: IP addresses, Device identifiers, Non-precise location data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## Sublime
Cookie duration: 396 (days).
Data collected and processed: IP addresses, Browsing and interaction data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## smartclip Europe GmbH
Cookie duration: 365 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Browsing and interaction data, User-provided data, Non-precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Ask Locala
Doesn't use cookies.
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Non-precise location data, Precise location data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Eyeota Pte Ltd
Cookie duration: 366 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Non-precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. 
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Azira
Doesn't use cookies.
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Browsing and interaction data, Non-precise location data, Precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## DoubleVerify Inc.
Doesn't use cookies.
Data collected and processed: IP addresses, Device characteristics, Probabilistic identifiers, Browsing and interaction data, Non-precise location data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Legitimate interest
## BIDSWITCH GmbH
Cookie duration: 365 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Authentication-derived identifiers, Browsing and interaction data, Non-precise location data, Precise location data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## IPONWEB GmbH
Cookie duration: 365 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Authentication-derived identifiers, Browsing and interaction data, User-provided data, Non-precise location data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## NextRoll, Inc.
Cookie duration: 395 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Browsing and interaction data, User-provided data, Non-precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. 
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## ID5 Technology SAS
Cookie duration: 90 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Authentication-derived identifiers, Browsing and interaction data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Teads France SAS
Cookie duration: 365 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Browsing and interaction data, Non-precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## digitalAudience B.V.
Cookie duration: 366 (days).
Data collected and processed: IP addresses, Device identifiers, Authentication-derived identifiers, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. 
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Ströer SSP GmbH (SSP)
Cookie duration: 365 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Browsing and interaction data, Non-precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## OS Data Solutions GmbH
Cookie duration: 90 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Authentication-derived identifiers, Browsing and interaction data, User-provided data, Non-precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## ConnectAd Demand GmbH
Cookie duration: 31 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. 
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Permodo GmbH
Doesn't use cookies.
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Browsing and interaction data, Non-precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Platform161 B.V.
Cookie duration: 396 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Browsing and interaction data, Non-precise location data, Precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Media.net Advertising FZ-LLC
Cookie duration: 396 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Authentication-derived identifiers, Browsing and interaction data, User-provided data, Non-precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## Connatix Native Exchange Inc.
Cookie duration: 31 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Browsing and interaction data, Non-precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## LiveIntent Inc.
Cookie duration: 731 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Authentication-derived identifiers, Browsing and interaction data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## ADman Interactive SLU
Cookie duration: 365 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, User-provided data, Non-precise location data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. 
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## LIFT DSP LIMITED
Cookie duration: 366 (days).
Data collected and processed: IP addresses, Browsing and interaction data, Non-precise location data
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## MADVERTISE MEDIA
Doesn't use cookies.
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, User-provided data, Non-precise location data, Precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## YOC AG
Cookie duration: 365 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Authentication-derived identifiers, Browsing and interaction data, User-provided data, Non-precise location data, Precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## AntVoice
Cookie duration: 403 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Authentication-derived identifiers, Browsing and interaction data, Non-precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Basis Global Technologies, Inc.
Cookie duration: 365 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Authentication-derived identifiers, Browsing and interaction data, Non-precise location data, Precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. 
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## Seedtag Advertising S.L
Cookie duration: 365 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Browsing and interaction data, Non-precise location data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Underdog Media LLC 
Cookie duration: 365 (days).
Data collected and processed: IP addresses, Device characteristics, Non-precise location data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Audience Solutions S.A.
Cookie duration: 365 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Authentication-derived identifiers, Browsing and interaction data, User-provided data, Non-precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. 
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## SMADEX, S.L.U.
Cookie duration: 365 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, User-provided data, Non-precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. 
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Bombora Inc.
Cookie duration: 365 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Authentication-derived identifiers, Browsing and interaction data, Non-precise location data, Users’ profiles
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## Outbrain UK.
Cookie duration: 396 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Browsing and interaction data, Non-precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Yieldmo, Inc.
Cookie duration: 365 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Authentication-derived identifiers, Browsing and interaction data, Non-precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. 
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## A Million Ads
Doesn't use cookies.
Data collected and processed: IP addresses, Device characteristics
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Hybrid Theory Global Ltd
Cookie duration: 365 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Authentication-derived identifiers, Browsing and interaction data, User-provided data, Non-precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Bidtellect, Inc
Cookie duration: 90 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Remerge GmbH
Doesn't use cookies.
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Browsing and interaction data, Non-precise location data
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## Affle Iberia SL
Cookie duration: 730 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Non-precise location data, Precise location data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## advanced store GmbH
Cookie duration: 365 (days).
Data collected and processed: Device identifiers
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## AdElement Media Solutions Pvt Ltd
Cookie duration: 365 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Browsing and interaction data, User-provided data, Non-precise location data, Precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. 
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## ADUX
Cookie duration: 720 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Non-precise location data, Precise location data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. 
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Magnite CTV, Inc.
Cookie duration: 366 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Browsing and interaction data, Non-precise location data, Precise location data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## Revcontent, LLC
Cookie duration: 400 (days).
Data collected and processed: IP addresses, Device characteristics, Probabilistic identifiers, Authentication-derived identifiers, Browsing and interaction data, User-provided data, Non-precise location data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## Hybrid Adtech GmbH
Cookie duration: 365 (days).
Data collected and processed: Device characteristics, Device identifiers
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Delta Projects AB
Cookie duration: 365 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Authentication-derived identifiers, Browsing and interaction data, User-provided data, Non-precise location data, Precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## Zemanta Inc.
Cookie duration: 1825 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Browsing and interaction data, Non-precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Mindlytix SAS
Cookie duration: 62 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Browsing and interaction data, Non-precise location data, Precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## adrule mobile GmbH
Cookie duration: 365 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Authentication-derived identifiers, Browsing and interaction data, Non-precise location data, Precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Publicis Media GmbH
Cookie duration: 1825 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Authentication-derived identifiers, Browsing and interaction data, User-provided data, Non-precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## M.D. Primis Technologies Ltd.
Cookie duration: 25 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Browsing and interaction data, User-provided data, Non-precise location data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## AcuityAds Inc.
Cookie duration: 365 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Authentication-derived identifiers, Browsing and interaction data, Non-precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. 
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## Rockerbox, Inc
Cookie duration: 30 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Authentication-derived identifiers, Browsing and interaction data, User-provided data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## VGI CTV, Inc
Cookie duration: 365 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Browsing and interaction data, Non-precise location data, Precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## StackAdapt Inc.
Cookie duration: 365 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Browsing and interaction data, Non-precise location data, Precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## OneTag Limited
Cookie duration: 396 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Browsing and interaction data, Non-precise location data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Cloud Technologies S.A.
Cookie duration: 365 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Authentication-derived identifiers, Browsing and interaction data, Non-precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. 
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Smartology Limited
Doesn't use cookies.
Data collected and processed: IP addresses
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## Tri-table Sp. z o.o.
Cookie duration: 366 (days).
Data collected and processed: Device characteristics, Probabilistic identifiers, Non-precise location data
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Yieldlove GmbH
Cookie duration: 30 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Browsing and interaction data, Non-precise location data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## Improve Digital
Cookie duration: 90 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Authentication-derived identifiers, Browsing and interaction data, User-provided data, Non-precise location data, Precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. 
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## Onnetwork Sp. z o.o.
Cookie duration: 50 (days).
Data collected and processed: IP addresses, Device characteristics
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. 
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## ADYOULIKE SA
Cookie duration: 365 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Browsing and interaction data, Non-precise location data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. 
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## DT Exchange (Digital Turbine (IL) Ltd.)
Doesn't use cookies.
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Nativo, Inc.
Cookie duration: 365 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Authentication-derived identifiers, Browsing and interaction data, Non-precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## Adobe Advertising Cloud
Cookie duration: 730 (days).
Data collected and processed: IP addresses, Device identifiers, Authentication-derived identifiers, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. 
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## A.Mob
Cookie duration: 395 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Authentication-derived identifiers, Browsing and interaction data, User-provided data, Non-precise location data, Precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Bannerflow AB
Cookie duration: 30 (days).
Data collected and processed: IP addresses, Device characteristics, Non-precise location data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. 
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## TabMo SAS
Cookie duration: 90 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Browsing and interaction data, User-provided data, Non-precise location data, Precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## ShowHeroes SRL
Cookie duration: 393 (days).
Data collected and processed: IP addresses, Device identifiers, Non-precise location data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## Integral Ad Science (incorporating ADmantX)
Doesn't use cookies.
Data collected and processed: IP addresses, Device characteristics, Browsing and interaction data, Non-precise location data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Legitimate interest
## Mirando GmbH & Co KG
Doesn't use cookies.
Data collected and processed: IP addresses, Device characteristics, Browsing and interaction data, Non-precise location data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Legitimate interest
## Open Web Technologies Ltd
Cookie duration: 365 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Browsing and interaction data, User-provided data, Non-precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## Wizaly
Cookie duration: 365 (days).
Data collected and processed: IP addresses, Device characteristics, Authentication-derived identifiers, Browsing and interaction data, Non-precise location data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Welect GmbH
Cookie duration: 14 (days).
Data collected and processed: IP addresses
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. 
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## Weborama
Cookie duration: 393 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Authentication-derived identifiers, Browsing and interaction data, User-provided data, Non-precise location data, Precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## Comcast International France SAS/FreeWheel Media
Cookie duration: 183 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Browsing and interaction data, Non-precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## Readpeak Oy
Cookie duration: 390 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Authentication-derived identifiers, Browsing and interaction data, User-provided data, Non-precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## SpringServe, LLC
Cookie duration: 364 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Browsing and interaction data, Non-precise location data, Precise location data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## Jivox Corporation
Cookie duration: 365 (days).
Data collected and processed: IP addresses, Device identifiers, Browsing and interaction data, Non-precise location data, Precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. 
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## Sojern, Inc.
Cookie duration: 365 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Browsing and interaction data, Non-precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Polar Mobile Group Inc.
Doesn't use cookies.
Data collected and processed: IP addresses, Device characteristics, Browsing and interaction data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Legitimate interest
## zeotap Data GmbH
Cookie duration: 365 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Authentication-derived identifiers, Browsing and interaction data, User-provided data, Non-precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Vistar Media EMEA BV
Doesn't use cookies.
Data collected and processed: Non-precise location data
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## On Device Research Limited
Cookie duration: 30 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Browsing and interaction data, User-provided data, Non-precise location data, Precise location data
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. 
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Mobfox US LLC
Cookie duration: 14 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Non-precise location data, Precise location data
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. 
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Exactag GmbH
Cookie duration: 180 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Authentication-derived identifiers, Browsing and interaction data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. 
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Celtra Inc.
Doesn't use cookies.
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Precise location data
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Accorp Sp. z o.o.
Cookie duration: 365 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Browsing and interaction data, User-provided data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Footballco Media Limited
Cookie duration: 396 (days).
Data collected and processed: IP addresses
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. 
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## ADTIMING TECHNOLOGY PTE. LTD
Cookie duration: 30 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Browsing and interaction data
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Gemius SA
Cookie duration: 1825 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Browsing and interaction data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## ad6media
Cookie duration: 365 (days).
Data collected and processed: IP addresses, Device characteristics, Probabilistic identifiers, Authentication-derived identifiers, Browsing and interaction data, Non-precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## InMobi Pte Ltd
Doesn't use cookies.
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Browsing and interaction data, User-provided data, Non-precise location data, Precise location data, Users’ profiles
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## SheMedia, LLC
Cookie duration: 365 (days).
Data collected and processed: IP addresses, Device characteristics, Probabilistic identifiers, Authentication-derived identifiers, Browsing and interaction data, User-provided data, Non-precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## DIGITEKA Technologies
Cookie duration: 397 (days).
Data collected and processed: IP addresses, Device characteristics, Browsing and interaction data, User-provided data, Non-precise location data, Precise location data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## The Kantar Group Limited
Cookie duration: 914 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Browsing and interaction data, Non-precise location data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Samba TV, Inc.
Cookie duration: 390 (days).
Data collected and processed: IP addresses, Device identifiers, Probabilistic identifiers, Browsing and interaction data, Non-precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. 
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Samba TV UK Limited
Cookie duration: 390 (days).
Data collected and processed: IP addresses, Device identifiers, Probabilistic identifiers, Browsing and interaction data, Non-precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. 
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Apester Ltd
Cookie duration: 400 (days).
Data collected and processed: Device identifiers, Browsing and interaction data, User-provided data, Non-precise location data
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## MGID Inc.
Cookie duration: 365 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Browsing and interaction data, Non-precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Seeding Alliance GmbH
Cookie duration: 3650 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Browsing and interaction data, Non-precise location data, Precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. 
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## Nielsen Media Research Ltd.
Cookie duration: 120 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Browsing and interaction data, User-provided data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Jakala Spain and Latam SL
Doesn't use cookies.
Data collected and processed: Device identifiers, Browsing and interaction data
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## RevX
Doesn't use cookies.
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Browsing and interaction data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Vidoomy Media SL
Cookie duration: 365 (days).
Data collected and processed: IP addresses, Device characteristics, Non-precise location data
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## The Reach Group GmbH
Cookie duration: 365 (days).
Data collected and processed: IP addresses, Device characteristics, Probabilistic identifiers, Browsing and interaction data, Non-precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. 
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Pixalate, Inc.
Cookie duration: 728 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Browsing and interaction data, Non-precise location data
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Triapodi Ltd. d/b/a Digital Turbine
Doesn't use cookies.
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## AudienceProject A/S
Cookie duration: 365 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Authentication-derived identifiers, Browsing and interaction data, User-provided data, Non-precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## Adtelligent Inc.
Cookie duration: 93 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Browsing and interaction data, User-provided data, Non-precise location data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Eulerian Technologies
Cookie duration: 390 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Authentication-derived identifiers, Browsing and interaction data, User-provided data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Seenthis AB
Doesn't use cookies.
Data collected and processed: IP addresses, Device characteristics
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
## travel audience GmbH
Cookie duration: 397 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Authentication-derived identifiers, Browsing and interaction data, Non-precise location data, Precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Proxi.cloud sp. z o.o.
Doesn't use cookies.
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Browsing and interaction data, Precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## HUMAN
Doesn't use cookies.
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Non-precise location data
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Legitimate interest
## SINGLESPOT SAS 
Doesn't use cookies.
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## INVIBES GROUP
Cookie duration: 365 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Authentication-derived identifiers, Browsing and interaction data, Non-precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## INVIDI technologies AB
Cookie duration: 3650 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Browsing and interaction data, User-provided data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## DEFINE MEDIA GMBH
Doesn't use cookies.
Data collected and processed: IP addresses, Device characteristics, Browsing and interaction data, Non-precise location data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## EX.CO Technologies Ltd 
Cookie duration: 30 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Non-precise location data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Targetspot Belgium SPRL
Doesn't use cookies.
Data collected and processed: IP addresses, Probabilistic identifiers, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Streamwise srl
Cookie duration: 366 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Authentication-derived identifiers, Browsing and interaction data, User-provided data, Non-precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Innovid LLC
Cookie duration: 90 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Browsing and interaction data, Non-precise location data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. 
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## uppr GmbH
Cookie duration: 365 (days).
Data collected and processed: User-provided data
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Zeta Global Corp.
Cookie duration: 390 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Browsing and interaction data, User-provided data, Non-precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Flexoffers.com, LLC
Cookie duration: 30 (days).
Data collected and processed: IP addresses, Device characteristics, Browsing and interaction data, User-provided data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## TAPTAP Digital SL
Cookie duration: 19 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Browsing and interaction data, User-provided data, Non-precise location data, Precise location data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. 
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## Madington
Doesn't use cookies.
Data collected and processed: IP addresses, Device characteristics, Probabilistic identifiers, Non-precise location data
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Legitimate interest
## Opinary (Affinity Global GmbH)
Cookie duration: 60 (days).
Data collected and processed: IP addresses, Device characteristics, Browsing and interaction data, User-provided data, Non-precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## GumGum, Inc.
Cookie duration: 90 (days).
Data collected and processed: IP addresses, Device characteristics, Browsing and interaction data, Non-precise location data
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. 
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## SevenData S.p.a.
Cookie duration: 180 (days).
Data collected and processed: Device characteristics, Device identifiers, Probabilistic identifiers, Browsing and interaction data
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Magnite, Inc. (Carbon AI Limited)
Cookie duration: 365 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Browsing and interaction data, Non-precise location data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## Automattic Ads
Cookie duration: 730 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Browsing and interaction data, User-provided data, Non-precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. 
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Arago
Doesn't use cookies.
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Authentication-derived identifiers, Browsing and interaction data, Non-precise location data, Precise location data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Alliance Gravity Data Media
Cookie duration: 3640 (days).
Data collected and processed: IP addresses, Device characteristics, Authentication-derived identifiers, Browsing and interaction data, Non-precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. 
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Cint USA, Inc.
Cookie duration: 730 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Browsing and interaction data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## One Tech Group GmbH
Cookie duration: 365 (days).
Data collected and processed: Device characteristics, Non-precise location data
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Legitimate interest
## Admixer EU GmbH
Cookie duration: 90 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, User-provided data, Non-precise location data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. 
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## Verve Group Europe GmbH
Doesn't use cookies.
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Authentication-derived identifiers, Browsing and interaction data, User-provided data, Non-precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## SunMedia 
Cookie duration: 120 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Non-precise location data
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Newsroom AI Ltd
Doesn't use cookies.
Data collected and processed: Device identifiers
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## The Ozone Project Limited
Cookie duration: 90 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Browsing and interaction data, Non-precise location data, Precise location data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. 
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Jampp LTD
Doesn't use cookies.
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Precise location data
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## Realtime Technologies GmbH
Doesn't use cookies.
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, User-provided data, Non-precise location data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## Smartclip Hispania S.L.
Cookie duration: Uses session cookies.
Data collected and processed: IP addresses, Device identifiers, Probabilistic identifiers, Browsing and interaction data, User-provided data, Non-precise location data, Users’ profiles
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## SmartyAds Inc.
Cookie duration: 14 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Browsing and interaction data, Non-precise location data, Precise location data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. 
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## DeepIntent, Inc.
Cookie duration: 548 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Non-precise location data
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. 
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## Happydemics
Doesn't use cookies.
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Authentication-derived identifiers, User-provided data, Non-precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## illuma technology limited
Doesn't use cookies.
Data collected and processed: Browsing and interaction data
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Legitimate interest
## Adhese
Cookie duration: 30 (days).
Data collected and processed: IP addresses, Device characteristics, Authentication-derived identifiers, User-provided data, Non-precise location data, Precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. 
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Radio Marketing Service interactive GmbH
Doesn't use cookies.
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Authentication-derived identifiers, Browsing and interaction data, User-provided data, Non-precise location data, Precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Otto GmbH & Co. KGaA
Cookie duration: 365 (days).
Data collected and processed: IP addresses, Device identifiers, Browsing and interaction data, User-provided data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## Adobe Audience Manager, Adobe Experience Platform
Cookie duration: 180 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Authentication-derived identifiers, Browsing and interaction data, User-provided data, Non-precise location data, Precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. 
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Next Different SpA
Cookie duration: 180 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Authentication-derived identifiers, Browsing and interaction data, Non-precise location data, Precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Kairos Fire
Doesn't use cookies.
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Non-precise location data, Precise location data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## ViewPay
Cookie duration: 30 (days).
Data collected and processed: IP addresses, Device characteristics
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. 
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## CHEQ AI TECHNOLOGIES
Cookie duration: 365 (days).
Data collected and processed: IP addresses, Device characteristics
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. 
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
## Dailymotion Video Player and Ad Products
Cookie duration: 396 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Authentication-derived identifiers, Browsing and interaction data, User-provided data, Non-precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## Goldbach Group AG
Cookie duration: 3653 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Authentication-derived identifiers, Browsing and interaction data, User-provided data, Non-precise location data, Precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## Mobilewalla, Inc.
Doesn't use cookies.
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Authentication-derived identifiers, Browsing and interaction data, User-provided data, Non-precise location data, Precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## Localsensor B.V.
Doesn't use cookies.
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Non-precise location data, Precise location data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Adjust Digital A/S
Doesn't use cookies.
Data collected and processed: IP addresses
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
## AllMediaDesk GmbH
Doesn't use cookies.
Data collected and processed: IP addresses
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## WebAds B.V
Doesn't use cookies.
Data collected and processed: IP addresses
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Online Solution
Cookie duration: 365 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Browsing and interaction data, User-provided data, Non-precise location data, Precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Impactify SARL
Cookie duration: 31 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Browsing and interaction data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## ucfunnel Co., Ltd.
Cookie duration: 365 (days).
Data collected and processed: Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Azerion Holding B.V.
Cookie duration: 366 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Browsing and interaction data, User-provided data, Non-precise location data, Precise location data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## Adnami Aps
Doesn't use cookies.
Data collected and processed: IP addresses, Non-precise location data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Legitimate interest
## Onfocus (Adagio)
Cookie duration: 60 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Browsing and interaction data, Non-precise location data, Precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## BEINTOO SPA
Cookie duration: 366 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Precise location data
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Blue
Cookie duration: 365 (days).
Data collected and processed: IP addresses, Device characteristics, Browsing and interaction data, Non-precise location data, Precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. 
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Seznam.cz, a.s.
Cookie duration: 366 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Authentication-derived identifiers, Browsing and interaction data, User-provided data, Non-precise location data, Precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## Hivestack Inc.
Doesn't use cookies.
Data collected and processed: Device identifiers, Precise location data
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## : Tappx
Cookie duration: 1 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Browsing and interaction data, Non-precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. 
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Relay42 Netherlands B.V.
Cookie duration: 730 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Browsing and interaction data, User-provided data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Smile Wanted Group
Cookie duration: 365 (days).
Data collected and processed: Device characteristics, Browsing and interaction data
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. 
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Gamoshi Ltd
Cookie duration: 30 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, User-provided data, Non-precise location data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Notify
Cookie duration: 365 (days).
Data collected and processed: User-provided data
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Axel Springer Teaser Ad GmbH
Cookie duration: 365 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Browsing and interaction data, Non-precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## TrueData Solutions, Inc.
Cookie duration: 913 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Authentication-derived identifiers, Browsing and interaction data, User-provided data, Non-precise location data, Precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Skaze
Cookie duration: 366 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Browsing and interaction data, Non-precise location data
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Smartme Analytics
Cookie duration: 371 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Browsing and interaction data, User-provided data, Precise location data
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. 
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## BLIINK SAS
Cookie duration: 396 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Browsing and interaction data, Non-precise location data
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Mobsuccess
Cookie duration: 365 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Browsing and interaction data, User-provided data, Non-precise location data, Precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Digital East GmbH
Cookie duration: 365 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Browsing and interaction data, Non-precise location data, Precise location data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. 
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## BeOp
Cookie duration: 366 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Authentication-derived identifiers, Browsing and interaction data, User-provided data, Non-precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## Liftoff Monetize and Vungle Exchange
Doesn't use cookies.
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Authentication-derived identifiers, Browsing and interaction data, User-provided data, Non-precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## MEDIA FORCE COMMUNICATIONS (2007) LTD
Cookie duration: 730 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Browsing and interaction data, Precise location data
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## Turk Telekom
Cookie duration: 180 (days).
Data collected and processed: IP addresses, Device identifiers, Non-precise location data, Precise location data, Users’ profiles
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. 
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## Intercept Interactive Inc. dba Undertone
Cookie duration: 366 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Browsing and interaction data, Non-precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. 
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## MyTraffic
Doesn't use cookies.
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Precise location data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Radio Net Media Limited
Cookie duration: 365 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Authentication-derived identifiers, Browsing and interaction data, User-provided data, Non-precise location data, Precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Blue Billywig Group BV
Cookie duration: 365 (days).
Data collected and processed: Device characteristics, Non-precise location data
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## The MediaGrid Inc.
Cookie duration: 365 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Browsing and interaction data, Non-precise location data, Precise location data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## MISSENA
Cookie duration: 360 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Authentication-derived identifiers, Browsing and interaction data, User-provided data, Non-precise location data, Users’ profiles
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Go.pl sp. z o.o.
Cookie duration: 3000 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Authentication-derived identifiers, Browsing and interaction data, User-provided data, Non-precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## HyperTV, Inc.
Cookie duration: 3650 (days).
Data collected and processed: IP addresses, Device characteristics, Probabilistic identifiers, Browsing and interaction data, User-provided data, Non-precise location data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. 
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## Reppublika Research and Analytics Austria GmbH
Cookie duration: 180 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Browsing and interaction data, Users’ profiles
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Dentsu Italia SpA
Cookie duration: 60 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Browsing and interaction data, Non-precise location data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. 
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## OneFootball GmbH
Cookie duration: 1825 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Browsing and interaction data, Users’ profiles
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## NC Audience Exchange, LLC 
Cookie duration: 365 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Authentication-derived identifiers, Browsing and interaction data, User-provided data, Non-precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## BidBerry SRL
Cookie duration: 365 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Authentication-derived identifiers, Browsing and interaction data, User-provided data, Non-precise location data, Precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## OnAudience Ltd
Cookie duration: 365 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Authentication-derived identifiers, Browsing and interaction data, Non-precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Audience Network
Cookie duration: 365 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Authentication-derived identifiers, Browsing and interaction data, Non-precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. 
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## XChange by SFBX®
Cookie duration: 365 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Authentication-derived identifiers, Browsing and interaction data, User-provided data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Online Advertising Network Sp. z o.o.
Cookie duration: 365 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Authentication-derived identifiers, Browsing and interaction data, Non-precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## impact.com
Cookie duration: 3650 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Browsing and interaction data
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. 
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## Adzymic Creavibes
Cookie duration: 365 (days).
Data collected and processed: Device characteristics, Probabilistic identifiers, Browsing and interaction data
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Between Exchange
Cookie duration: 365 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Browsing and interaction data, Non-precise location data
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. 
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## Pubfinity LLC
Cookie duration: 3650 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Authentication-derived identifiers, Browsing and interaction data, User-provided data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Pinpoll GmbH
Cookie duration: 30 (days).
Data collected and processed: IP addresses, User-provided data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Appier PTE Ltd
Cookie duration: 365 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Authentication-derived identifiers, Browsing and interaction data, User-provided data, Non-precise location data, Precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## LetThereBeAds / Performax
Cookie duration: 90 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Browsing and interaction data, Non-precise location data
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## Anzu Virtual Reality LTD
Doesn't use cookies.
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Browsing and interaction data, User-provided data, Non-precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## BidMachine Inc.
Doesn't use cookies.
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Authentication-derived identifiers, Browsing and interaction data, User-provided data, Non-precise location data, Precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## Monet Engine Inc
Cookie duration: 365 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Authentication-derived identifiers, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## adbility media GmbH
Cookie duration: 365 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Non-precise location data
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Legitimate interest
## 6Sense Insights, Inc.
Cookie duration: 731 (days).
Data collected and processed: IP addresses, Probabilistic identifiers, Browsing and interaction data, Non-precise location data, Users’ profiles
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## Vidazoo Ltd
Cookie duration: 31 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Browsing and interaction data, Precise location data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Justtag Sp. z o.o.
Doesn't use cookies.
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Authentication-derived identifiers, Non-precise location data, Precise location data, Users’ profiles
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Adxperience SAS
Doesn't use cookies.
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Non-precise location data, Precise location data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## AUDIOMOB LTD
Doesn't use cookies.
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Browsing and interaction data, Non-precise location data, Precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Legitimate interest
## THE NEWCO S.R.L.
Cookie duration: 1 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Authentication-derived identifiers, Browsing and interaction data, User-provided data, Non-precise location data, Precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Kiosked Ltd
Doesn't use cookies.
Data collected and processed: IP addresses, Device characteristics, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Legitimate interest
## targeting360 GmbH
Cookie duration: 90 (days).
Data collected and processed: IP addresses
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. 
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Google Advertising Products
Cookie duration: 396 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Authentication-derived identifiers, Browsing and interaction data, User-provided data, Non-precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## GfK GmbH
Cookie duration: 730 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Authentication-derived identifiers, Browsing and interaction data, User-provided data, Non-precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## RevJet
Cookie duration: 365 (days).
Data collected and processed: IP addresses, Device identifiers, Non-precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. 
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Protected Media LTD
Doesn't use cookies.
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Browsing and interaction data
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Legitimate interest
## Clinch Labs LTD
Cookie duration: 730 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Browsing and interaction data, Non-precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. 
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## MEDIAMETRIE
Cookie duration: 390 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Browsing and interaction data, Non-precise location data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## MARKETPERF CORP
Cookie duration: 365 (days).
Data collected and processed: IP addresses, Device characteristics, Probabilistic identifiers, Authentication-derived identifiers, Browsing and interaction data, Non-precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## adtron technologies GmbH
Cookie duration: 1 (days).
Data collected and processed: Device characteristics, Browsing and interaction data, Non-precise location data
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## SelectMedia International LTD
Cookie duration: 90 (days).
Data collected and processed: IP addresses
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Mars Media Group
Doesn't use cookies.
Data collected and processed: Device identifiers
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Discover-Tech ltd
Doesn't use cookies.
Data collected and processed: IP addresses, Device identifiers
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Adtarget Teknoloji A.S.
Cookie duration: 93 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Browsing and interaction data, User-provided data, Non-precise location data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Aniview LTD
Cookie duration: 90 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Browsing and interaction data, Non-precise location data
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## FeedAd GmbH
Cookie duration: 30 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Browsing and interaction data, User-provided data, Non-precise location data, Precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## Audienzz AG
Cookie duration: 365 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Authentication-derived identifiers, Browsing and interaction data, Non-precise location data, Users’ profiles
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Hearts and Science München GmbH
Cookie duration: 60 (days).
Data collected and processed: IP addresses
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. 
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Ad Alliance GmbH
Cookie duration: 365 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Authentication-derived identifiers, Browsing and interaction data, User-provided data, Users’ profiles
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Media Square
Cookie duration: 90 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. 
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Amazon Ads
Cookie duration: 396 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Authentication-derived identifiers, Browsing and interaction data, Non-precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Factor Eleven GmbH
Cookie duration: 30 (days).
Data collected and processed: IP addresses, Device characteristics, Non-precise location data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. 
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Artefact Deutschland GmbH
Cookie duration: 365 (days).
Data collected and processed: Non-precise location data
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Adpone SL
Cookie duration: 120 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Non-precise location data
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Reppublika Data Analytics and Technologies GmbH
Cookie duration: 180 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Browsing and interaction data, Users’ profiles
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Bannernow, Inc.
Doesn't use cookies.
Data collected and processed: IP addresses, Device characteristics
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Legitimate interest
## POWERENGINE PTE.LIMITED
Cookie duration: 1 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. 
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## LinkedIn Ireland Unlimited Company
Cookie duration: 365 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Authentication-derived identifiers, Browsing and interaction data, Non-precise location data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## Aarki, Inc.
Doesn't use cookies.
Data collected and processed: IP addresses, Device characteristics, Device identifiers, User-provided data, Non-precise location data
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## Moloco, Inc.
Cookie duration: 730 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Non-precise location data
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## lead alliance GmbH
Cookie duration: 90 (days).
Data collected and processed: IP addresses, Browsing and interaction data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## iPROM
Cookie duration: 365 (days).
Data collected and processed: IP addresses, Device identifiers, Non-precise location data, Precise location data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Nielsen International SA
Cookie duration: 390 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, User-provided data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## Blockthrough, Inc.
Cookie duration: 90 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Non-precise location data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## NoBid, Inc.
Cookie duration: 7 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Non-precise location data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. 
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## retailAds GmbH & Co. KG
Cookie duration: 90 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Browsing and interaction data, Non-precise location data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## Kameleoon SAS
Cookie duration: 365 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Non-precise location data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## vitrado GmbH
Cookie duration: 365 (days).
Data collected and processed: IP addresses, Device characteristics, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. 
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Adverty AB (publ)
Doesn't use cookies.
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Browsing and interaction data, User-provided data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## TX Group AG
Cookie duration: 365 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Authentication-derived identifiers, Browsing and interaction data, User-provided data, Precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## United Internet Media GmbH
Cookie duration: 365 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Authentication-derived identifiers, Browsing and interaction data, Non-precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. 
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Disqus
Cookie duration: 365 (days).
Data collected and processed: IP addresses, Device characteristics, Probabilistic identifiers, Authentication-derived identifiers, Browsing and interaction data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. 
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## PixFuture Media Inc.
Cookie duration: 365 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Non-precise location data, Precise location data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## GeoEdge
Doesn't use cookies.
Data collected and processed: IP addresses, Device characteristics, Non-precise location data
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Legitimate interest
## Epom
Cookie duration: 730 (days).
Data collected and processed: IP addresses, Device characteristics, Non-precise location data
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Publisher First, Inc.
Cookie duration: 7 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Authentication-derived identifiers, Browsing and interaction data, User-provided data, Non-precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Strossle International AB
Doesn't use cookies.
Data collected and processed: IP addresses, Device identifiers, Non-precise location data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## Petal Ads
Doesn't use cookies.
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Browsing and interaction data, User-provided data, Non-precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## SOMQUERY SOMTAG - (SevenOne Media)
Cookie duration: 365 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Browsing and interaction data, User-provided data, Non-precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## Publica LLC
Cookie duration: 60 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Truvid Inc.
Cookie duration: 60 (days).
Data collected and processed: Device characteristics, User-provided data, Non-precise location data
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## I.R.V. D.O.O.
Cookie duration: 730 (days).
Data collected and processed: IP addresses, Device characteristics, Probabilistic identifiers, Browsing and interaction data, Non-precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## HEIMSPIEL Medien GmbH & Co. KG
Cookie duration: 2 (days).
Data collected and processed: IP addresses, Device characteristics, Non-precise location data
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. 
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Mintegral International Limited
Doesn't use cookies.
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Browsing and interaction data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## Brave People Ltd.
Doesn't use cookies.
Data collected and processed: IP addresses, Device identifiers, Browsing and interaction data, Non-precise location data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Webgains GmbH
Cookie duration: 365 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## PRECISO SRL
Cookie duration: 360 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Browsing and interaction data, User-provided data, Non-precise location data, Users’ profiles
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Experian LTD
Cookie duration: 183 (days).
Data collected and processed: IP addresses, Device identifiers, Probabilistic identifiers, Authentication-derived identifiers, Non-precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Natív Hirdetés Korlátolt Felelősségű Társaság
Cookie duration: 60 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Non-precise location data
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. 
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## Quantyoo GmbH & Co. KG
Cookie duration: 365 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Authentication-derived identifiers, Browsing and interaction data, User-provided data, Non-precise location data, Precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Hillside (Sports) GP Limited
Cookie duration: 5 (days).
Data collected and processed: IP addresses, Device characteristics, Probabilistic identifiers, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Online Media Solutions LTD 
Doesn't use cookies.
Data collected and processed: IP addresses, Device characteristics, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Legitimate interest
## Listonic Sp. z o.o.
Cookie duration: 400 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Authentication-derived identifiers, Browsing and interaction data, User-provided data, Non-precise location data, Precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## Dianomi PLC
Cookie duration: 1827 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Browsing and interaction data, User-provided data, Non-precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## Gadsme
Doesn't use cookies.
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Non-precise location data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## ANINPRO-CREATIVE, S.L.
Cookie duration: 30 (days).
Data collected and processed: IP addresses, Browsing and interaction data, User-provided data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Threedium Ltd
Doesn't use cookies.
Data collected and processed: Device characteristics, Device identifiers, Browsing and interaction data, Non-precise location data
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## IPSOS MORI UK LTD
Cookie duration: 365 (days).
Data collected and processed: IP addresses, Device characteristics, Probabilistic identifiers, Browsing and interaction data, Non-precise location data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Mobkoi Ltd
Cookie duration: 16 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Browsing and interaction data, Non-precise location data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Advisible AB
Cookie duration: 365 (days).
Data collected and processed: IP addresses, Device characteristics, Non-precise location data
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. 
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## Insticator, Inc.
Cookie duration: 30 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Authentication-derived identifiers, Browsing and interaction data, User-provided data, Non-precise location data, Precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Redbranch, Inc dba Fraudlogix
Doesn't use cookies.
Data collected and processed: IP addresses, Device characteristics
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Legitimate interest
## Opti Digital SAS
Cookie duration: 90 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Authentication-derived identifiers, Browsing and interaction data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## SPORTORITY UK LTD
Cookie duration: 30 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Browsing and interaction data, User-provided data, Non-precise location data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## Livewrapped AB
Cookie duration: 30 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Authentication-derived identifiers, User-provided data, Non-precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## Bertelsmann Data Service GmbH
Cookie duration: 365 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Authentication-derived identifiers, Browsing and interaction data, User-provided data, Precise location data, Users’ profiles
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. 
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Dentsu Product & Services GmbH
Cookie duration: 356 (days).
Data collected and processed: IP addresses, Device characteristics, Probabilistic identifiers, Authentication-derived identifiers, Browsing and interaction data, Non-precise location data, Precise location data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Alphalyr SAS
Cookie duration: 30 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Authentication-derived identifiers, Browsing and interaction data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## IQM CORPORATION
Cookie duration: 15 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Non-precise location data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. 
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Traffective GmbH
Cookie duration: 365 (days).
Data collected and processed: IP addresses, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## DIGITAL SQUAD
Cookie duration: 396 (days).
Data collected and processed: Device characteristics
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## SoD ScreenOnDemand GmbH
Cookie duration: 365 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Browsing and interaction data, User-provided data, Non-precise location data, Precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## dataXtrade GmbH
Cookie duration: 365 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Browsing and interaction data, User-provided data, Non-precise location data, Precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Toluna Netherlands B.V. KvK
Cookie duration: 730 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Browsing and interaction data, User-provided data
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Marfeel Solutions, SL (Compass)
Cookie duration: 365 (days).
Data collected and processed: IP addresses, Device characteristics, Browsing and interaction data, Non-precise location data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## ProSiebenSat.1 Digital Data GmbH
Cookie duration: 730 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Authentication-derived identifiers, Browsing and interaction data, User-provided data, Non-precise location data, Precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Caroda s.r.o.
Doesn't use cookies.
Data collected and processed: IP addresses, Device characteristics, Browsing and interaction data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Konodrac S.L.
Cookie duration: 365 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Authentication-derived identifiers, Browsing and interaction data, User-provided data, Non-precise location data, Precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. 
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## adWMG
Cookie duration: 90 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. 
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Tangoo S.R.L.
Cookie duration: 360 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Browsing and interaction data, User-provided data, Non-precise location data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## CIBLECLIC
Cookie duration: 183 (days).
Data collected and processed: Device characteristics, User-provided data
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Nexx360
Cookie duration: 180 (days).
Data collected and processed: IP addresses, Device characteristics, Non-precise location data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## socoto gmbh & co. kg
Doesn't use cookies.
Data collected and processed: IP addresses
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## glomex GmbH
Doesn't use cookies.
Data collected and processed: IP addresses, Device characteristics, Probabilistic identifiers, Browsing and interaction data, Non-precise location data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## WEMASS MEDIA AUDIENCE SAFE SOLUTIONS, S.L. 
Cookie duration: 1095 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Browsing and interaction data, Non-precise location data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Kargo Global Inc.
Cookie duration: 365 (days).
Data collected and processed: IP addresses, Device characteristics, Probabilistic identifiers, Browsing and interaction data, Non-precise location data
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Cluep Inc.
Doesn't use cookies.
Data collected and processed: IP addresses, Device characteristics, Device identifiers, User-provided data, Non-precise location data, Precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Pelmorex Corp.
Cookie duration: 365 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Browsing and interaction data, Non-precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Netpoint Media GmbH
Cookie duration: 1 (days).
Data collected and processed: Browsing and interaction data
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## TikTok Ad Network
Doesn't use cookies.
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Browsing and interaction data, User-provided data, Non-precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## Media16 ltd
Doesn't use cookies.
Data collected and processed: IP addresses
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## QUARTER MEDIA GmbH
Cookie duration: 90 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Browsing and interaction data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Leadoo Marketing Technologies Ltd
Doesn't use cookies.
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Authentication-derived identifiers, Browsing and interaction data, User-provided data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## Hashtag Labs Inc.
Cookie duration: 390 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Browsing and interaction data, User-provided data, Non-precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## CMI Marketing, Inc. d/b/a Raptive
Cookie duration: 359 (days).
Data collected and processed: IP addresses, Probabilistic identifiers, Authentication-derived identifiers, Browsing and interaction data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## EXOCLICK, S.L.
Cookie duration: 730 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Browsing and interaction data, Non-precise location data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. 
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## Luna Media Group LLC
Cookie duration: 14 (days).
Data collected and processed: Device characteristics
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## ADSTOURS SAS
Cookie duration: 730 (days).
Data collected and processed: IP addresses, Browsing and interaction data, Non-precise location data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. 
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## wetter.com Group GmbH
Doesn't use cookies.
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Browsing and interaction data, Non-precise location data, Precise location data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Extreme Reach, Inc
Cookie duration: 180 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Browsing and interaction data, Non-precise location data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. 
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Mobility-Ads GmbH
Cookie duration: 30 (days).
Data collected and processed: IP addresses, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## VUUKLE DMCC
Cookie duration: 365 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Authentication-derived identifiers, Browsing and interaction data, User-provided data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Somplo Ltd
Doesn't use cookies.
Data collected and processed: IP addresses, Device characteristics
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Legitimate interest
## Onesoon Limited t/a Adalyser
Cookie duration: 730 (days).
Data collected and processed: IP addresses, Device identifiers
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## VLYBY Digital GmbH
Doesn't use cookies.
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Browsing and interaction data, Non-precise location data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## FUNKE Digital GmbH
Cookie duration: 366 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, User-provided data
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Adelaide Metrics Inc
Doesn't use cookies.
Data collected and processed: Device characteristics, Browsing and interaction data
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Legitimate interest
## Baidu (Hong Kong) Limited
Cookie duration: 366 (days).
Data collected and processed: Browsing and interaction data
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Ringier Axel Springer Polska sp. z o.o.
Cookie duration: 390 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Browsing and interaction data, User-provided data, Non-precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## AdView
Doesn't use cookies.
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Non-precise location data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## THE LINEA 1 MKT SL
Cookie duration: 365 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Authentication-derived identifiers, Browsing and interaction data, Non-precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## crossvertise GmbH
Doesn't use cookies.
Data collected and processed: Non-precise location data
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Sparteo
Cookie duration: 365 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Browsing and interaction data, Non-precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## Dentsu A/S
Cookie duration: 822 (days).
Data collected and processed: IP addresses, Device characteristics, Authentication-derived identifiers, Browsing and interaction data, Users’ profiles
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Havas Media (Artemis Alliance S.L.U.)
Doesn't use cookies.
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Browsing and interaction data, User-provided data, Users’ profiles
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Project Agora Ltd
Doesn't use cookies.
Data collected and processed: Device characteristics, Browsing and interaction data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## VIADS ADVERTISING S.L.
Cookie duration: 30 (days).
Data collected and processed: IP addresses
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## Pressboard Media Inc
Doesn't use cookies.
Data collected and processed: IP addresses, Probabilistic identifiers, Browsing and interaction data
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## AA INTERNET-MEDIA Ltd
Cookie duration: 3650 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Browsing and interaction data, Non-precise location data
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. 
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Sonic Odeeo ltd
Doesn't use cookies.
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## Sqreem Technologies Private Limited
Doesn't use cookies.
Data collected and processed: IP addresses, Device identifiers
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Legitimate interest
## TypeA Holdings Ltd
Cookie duration: 30 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## TMT Digital Inc
Doesn't use cookies.
Data collected and processed: IP addresses
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
## Resono B.V.
Doesn't use cookies.
Data collected and processed: IP addresses, Device identifiers, Non-precise location data, Precise location data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## JWP, Inc.
Doesn't use cookies.
Data collected and processed: Device characteristics, Probabilistic identifiers
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Questpass Sp. z o.o.
Doesn't use cookies.
Data collected and processed: IP addresses, Device characteristics, Browsing and interaction data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## OnProspects Ltd
Cookie duration: 365 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Authentication-derived identifiers, Browsing and interaction data, Non-precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. 
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Gamesight Inc
Cookie duration: 365 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Authentication-derived identifiers, Browsing and interaction data, Non-precise location data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. 
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Ströer Media Solutions GmbH
Doesn't use cookies.
Data collected and processed: IP addresses, Device characteristics, Device identifiers, User-provided data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## Next Millennium Media INC
Cookie duration: 365 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Browsing and interaction data, Non-precise location data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. 
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## onlineumfragen.com GmbH
Cookie duration: Uses session cookies.
Data collected and processed: IP addresses, Probabilistic identifiers, User-provided data
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Evorra Ltd
Cookie duration: 365 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Authentication-derived identifiers, Browsing and interaction data, User-provided data, Non-precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Doceree UK Limited
Cookie duration: 365 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Authentication-derived identifiers, Browsing and interaction data, User-provided data, Non-precise location data, Precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Arpeely Ltd.
Cookie duration: 90 (days).
Data collected and processed: IP addresses
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. 
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## Italiaonline S.p.A.
Cookie duration: 180 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Authentication-derived identifiers, Browsing and interaction data, User-provided data, Non-precise location data, Precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## BCOVERY SAS
Doesn't use cookies.
Data collected and processed: IP addresses, Device characteristics, Browsing and interaction data, Non-precise location data, Precise location data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## Clever Advertising
Cookie duration: 30 (days).
Data collected and processed: IP addresses, Device characteristics
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. 
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## Adventure Media SARL
Cookie duration: 3650 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Browsing and interaction data, Non-precise location data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. 
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## dpa-infocom GmbH
Doesn't use cookies.
Data collected and processed: Browsing and interaction data
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Legitimate interest
## Snigel Web Services Limited
Cookie duration: 90 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Authentication-derived identifiers, Browsing and interaction data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## CITISERVI EUROPE, S.L.
Cookie duration: 58 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Authentication-derived identifiers, User-provided data, Non-precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Seven Technologies S.L.
Cookie duration: 30 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Non-precise location data, Precise location data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## EXADS
Cookie duration: 730 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Browsing and interaction data, Non-precise location data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. 
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## Njuice AB
Cookie duration: 400 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Browsing and interaction data, Non-precise location data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## CASTOOLA D.O.O.
Cookie duration: 365 (days).
Data collected and processed: IP addresses, Device characteristics, Browsing and interaction data, User-provided data, Non-precise location data, Precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## Score Media Group GmbH & Co. KG
Cookie duration: 90 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Authentication-derived identifiers, Browsing and interaction data, User-provided data, Non-precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. 
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## ADMAX
Doesn't use cookies.
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Non-precise location data, Precise location data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Relevant Digital Oy
Cookie duration: 90 (days).
Data collected and processed: IP addresses
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. 
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## PIA Advertising GmbH
Cookie duration: 90 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Authentication-derived identifiers, Browsing and interaction data, User-provided data, Non-precise location data, Precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. 
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Capaneo GmbH
Doesn't use cookies.
Data collected and processed: IP addresses, Device identifiers, Precise location data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Covatic Ltd
Doesn't use cookies.
Data collected and processed: IP addresses, Device characteristics, Authentication-derived identifiers, Browsing and interaction data, User-provided data, Non-precise location data, Users’ profiles
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Better Ads GmbH
Cookie duration: 60 (days).
Data collected and processed: Browsing and interaction data, Non-precise location data
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## FRVR Limited
Cookie duration: 730 (days).
Data collected and processed: Device characteristics, Probabilistic identifiers, Browsing and interaction data, User-provided data, Non-precise location data
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## KÖNIGSTEINER digital GmbH
Cookie duration: 365 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Non-precise location data
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. 
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## 152 Media LLC
Cookie duration: 90 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Browsing and interaction data, Non-precise location data, Precise location data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Hubvisor
Doesn't use cookies.
Data collected and processed: Device characteristics, Non-precise location data
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Shopfully GmbH
Cookie duration: 784 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Browsing and interaction data, User-provided data, Non-precise location data, Precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Anonymised
Cookie duration: 365 (days).
Data collected and processed: IP addresses, Device characteristics, Browsing and interaction data, User-provided data, Non-precise location data, Users’ profiles
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## REMAILME
Cookie duration: 365 (days).
Data collected and processed: IP addresses, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Media-Micro-Census GmbH
Doesn't use cookies.
Data collected and processed: IP addresses, Device characteristics, Probabilistic identifiers, Authentication-derived identifiers, Browsing and interaction data, Non-precise location data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## TF1 PUBLICITE
Cookie duration: 183 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Authentication-derived identifiers, Browsing and interaction data, User-provided data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Microsoft Advertising
Cookie duration: 396 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Authentication-derived identifiers, Browsing and interaction data, User-provided data, Non-precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## MobUpps International LTD
Cookie duration: 730 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Non-precise location data
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. 
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Lupon Media
Cookie duration: 30 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Authentication-derived identifiers, Browsing and interaction data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Nativery Srl
Cookie duration: 365 (days).
Data collected and processed: IP addresses, Device characteristics
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Bidmatic Inc
Cookie duration: 93 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Browsing and interaction data, User-provided data, Non-precise location data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Opera Software Ireland Limited
Cookie duration: 365 (days).
Data collected and processed: IP addresses, Device identifiers, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. 
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## Infolinks Media, LLC
Cookie duration: 365 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Browsing and interaction data, Non-precise location data
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Verasity Limited
Cookie duration: 365 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Browsing and interaction data, Non-precise location data, Precise location data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Viafoura Inc.
Cookie duration: 365 (days).
Data collected and processed: IP addresses, Authentication-derived identifiers, Browsing and interaction data, User-provided data
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## CleverPush GmbH
Doesn't use cookies.
Data collected and processed: IP addresses, Device characteristics, Device identifiers
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Agate Systems Limited
Cookie duration: 30 (days).
Data collected and processed: Device characteristics, Device identifiers, Browsing and interaction data, User-provided data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. 
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## xpln.ai SAS
Doesn't use cookies.
Data collected and processed: IP addresses, Device characteristics, Browsing and interaction data, Non-precise location data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Legitimate interest
## ORANGE CLICK MEDIA & COMMERCE LTD
Cookie duration: 400 (days).
Data collected and processed: IP addresses, Device characteristics, Probabilistic identifiers, Browsing and interaction data, Non-precise location data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## AdInMo LTD
Doesn't use cookies.
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## Boldwin LTD
Doesn't use cookies.
Data collected and processed: IP addresses
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Sonares GmbH
Cookie duration: 31 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Authentication-derived identifiers, Browsing and interaction data, User-provided data, Non-precise location data, Precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## ividence
Cookie duration: 390 (days).
Data collected and processed: IP addresses, Device characteristics, Authentication-derived identifiers, Browsing and interaction data, User-provided data, Non-precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. 
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## Refine Direct Srl
Doesn't use cookies.
Data collected and processed: IP addresses, Device characteristics, Probabilistic identifiers
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Live Data Solutions SL
Doesn't use cookies.
Data collected and processed: IP addresses, Device characteristics
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## streaMonkey GmbH
Doesn't use cookies.
Data collected and processed: IP addresses
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
## ADTTRIBUTION Inc
Cookie duration: 365 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Authentication-derived identifiers, Browsing and interaction data, Non-precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. 
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Kueez Entertainment Ltd.
Cookie duration: 30 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Browsing and interaction data, Non-precise location data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## Alkimi
Cookie duration: Uses session cookies.
Data collected and processed: IP addresses, Device characteristics, Device identifiers, User-provided data, Non-precise location data, Precise location data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Sitewit, Corp
Cookie duration: 90 (days).
Data collected and processed: IP addresses, Device characteristics, User-provided data, Non-precise location data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
## Arcanor Bilgi Teknolojileri ve Hizmetleri A.Ş.
Doesn't use cookies.
Data collected and processed: Device identifiers, Precise location data
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## Synamedia
Doesn't use cookies.
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Authentication-derived identifiers, Browsing and interaction data, Non-precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Holid AB
Cookie duration: 90 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Browsing and interaction data, Non-precise location data, Precise location data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## Raptor Services a/s
Cookie duration: 365 (days).
Data collected and processed: IP addresses, Authentication-derived identifiers, Browsing and interaction data, User-provided data, Users’ profiles
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. 
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## BotTalk UG (haftungsbeschränkt)
Cookie duration: 30 (days).
Data collected and processed: Device characteristics
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. 
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Anteriad, LLC
Cookie duration: 366 (days).
Data collected and processed: IP addresses, Non-precise location data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. 
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## SSMas
Doesn't use cookies.
Data collected and processed: IP addresses, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Prisma Media
Doesn't use cookies.
Data collected and processed: IP addresses, Probabilistic identifiers, Authentication-derived identifiers, Browsing and interaction data, Users’ profiles
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## AccountInsight Ltd
Doesn't use cookies.
Data collected and processed: IP addresses
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
## Loop Now Technologies Inc.
Doesn't use cookies.
Data collected and processed: IP addresses
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## ResponsiveAds, Inc.
Doesn't use cookies.
Data collected and processed: IP addresses, Device characteristics, Browsing and interaction data, User-provided data, Non-precise location data, Precise location data
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## ArcSpan Technologies, Inc.
Doesn't use cookies.
Data collected and processed: IP addresses, Device characteristics, Browsing and interaction data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## Amplified IntelligenceTechnologies
Doesn't use cookies.
Data collected and processed: IP addresses, Device characteristics, Browsing and interaction data, Non-precise location data
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Legitimate interest
## MEDIAWAYSS Sp. z o.o.
Cookie duration: 364 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Browsing and interaction data, Non-precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. 
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Gameloft SE
Doesn't use cookies.
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, User-provided data, Non-precise location data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Edge226 Ltd
Doesn't use cookies.
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Non-precise location data
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Aderize, Inc.
Doesn't use cookies.
Data collected and processed: Browsing and interaction data, Non-precise location data
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Legitimate interest
## fraud0 GmbH
Doesn't use cookies.
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Browsing and interaction data
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Legitimate interest
## Adasta Media S.r.l.
Cookie duration: 396 (days).
Data collected and processed: IP addresses, Browsing and interaction data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## CND Motion Media GmbH
Cookie duration: 28 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Browsing and interaction data, Users’ profiles
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. 
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Feeltapmedia Limited
Doesn't use cookies.
Data collected and processed: IP addresses, Device characteristics, Device identifiers
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## Viomba Oy
Doesn't use cookies.
Data collected and processed: IP addresses, Device characteristics, Non-precise location data
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## Memob Plus FZ LLC
Cookie duration: 365 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Browsing and interaction data, User-provided data, Precise location data, Users’ profiles
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. 
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Clickagy LLC
Cookie duration: 729 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Authentication-derived identifiers, Browsing and interaction data, Non-precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. 
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Zuuvi ApS
Doesn't use cookies.
Data collected and processed: IP addresses, Device characteristics, Non-precise location data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## R2B2 a.s.
Cookie duration: 90 (days).
Data collected and processed: IP addresses, Device characteristics, Non-precise location data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## FireArc Technologies Ltd
Cookie duration: 7995 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Browsing and interaction data, Non-precise location data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. 
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## Empower AdTech
Cookie duration: 365 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Authentication-derived identifiers, Browsing and interaction data, User-provided data, Non-precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## YIELDBIRD SP. Z O.O.
Cookie duration: 90 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## Publicis One Spain S.L.
Cookie duration: 58 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Browsing and interaction data, Non-precise location data, Precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Optima Network SL
Cookie duration: 120 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Non-precise location data
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Adventive Tech, Inc.
Cookie duration: 100 (days).
Data collected and processed: IP addresses, Device characteristics, Non-precise location data
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## ABCS INSIGHTS
Doesn't use cookies.
Data collected and processed: IP addresses
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Adwatch S.L.
Doesn't use cookies.
Data collected and processed: Device characteristics, Probabilistic identifiers, Browsing and interaction data, Non-precise location data
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Sabio London Limited
Cookie duration: 365 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Non-precise location data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## TStack Inc
Cookie duration: 731 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Browsing and interaction data, User-provided data, Non-precise location data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## Airtory Inc
Doesn't use cookies.
Data collected and processed: IP addresses, Device identifiers, User-provided data, Non-precise location data
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## NinaData Oy
Cookie duration: 2486 (days).
Data collected and processed: Non-precise location data
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Creatopy INC
Doesn't use cookies.
Data collected and processed: IP addresses, Device characteristics, Non-precise location data
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Legitimate interest
## Xapads Media Ltd
Cookie duration: 365 (days).
Data collected and processed: IP addresses, Device identifiers, Non-precise location data, Precise location data, Users’ profiles
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. 
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## Blue Dawn Marketing Consulting Group S.L.
Cookie duration: 365 (days).
Data collected and processed: IP addresses, Device characteristics, Browsing and interaction data, Non-precise location data, Precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. 
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Intent IQ LLC
Cookie duration: 730 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Authentication-derived identifiers, Browsing and interaction data, User-provided data, Non-precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## ConceptX ApS
Cookie duration: 90 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Browsing and interaction data, Non-precise location data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. 
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## Affle Inc
Doesn't use cookies.
Data collected and processed: IP addresses, Device identifiers
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Mobian LLC
Doesn't use cookies.
Data collected and processed: IP addresses, Device identifiers, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Transfon Ltd
Cookie duration: 396 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Authentication-derived identifiers, Browsing and interaction data, User-provided data, Non-precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Admaster Private Limited
Cookie duration: 365 (days).
Data collected and processed: IP addresses, Device identifiers, Probabilistic identifiers, Browsing and interaction data, Non-precise location data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Bidease Inc
Doesn't use cookies.
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Non-precise location data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## AnyClip Inc.
Cookie duration: 30 (days).
Data collected and processed: Device characteristics, Non-precise location data
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Pubstack
Cookie duration: 180 (days).
Data collected and processed: IP addresses, Device characteristics, Browsing and interaction data, Non-precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Intango Ltd
Doesn't use cookies.
Data collected and processed: IP addresses, Device characteristics, Probabilistic identifiers, Non-precise location data, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Legitimate interest
## THEADX YAZILIM HİZMETLERİ SAN.VE TİC.A.Ş
Cookie duration: 540 (days).
Data collected and processed: Device identifiers, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. 
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Pixels AI Ltd
Cookie duration: 365 (days).
Data collected and processed: IP addresses, Device characteristics, Browsing and interaction data
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## zeotap GmbH
Cookie duration: 365 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Authentication-derived identifiers, Browsing and interaction data, User-provided data, Non-precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Pubx AI LTD
Doesn't use cookies.
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Authentication-derived identifiers, User-provided data, Non-precise location data
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Persona.ly
Doesn't use cookies.
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Browsing and interaction data, Non-precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
ConsentLegitimate interest
## Peer39
Doesn't use cookies.
Data collected and processed: IP addresses
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
## Yahoo International Limited
Cookie duration: 750 (days).
Data collected and processed: IP addresses, Device characteristics, Device identifiers, Probabilistic identifiers, Authentication-derived identifiers, Browsing and interaction data, User-provided data, Non-precise location data, Precise location data, Users’ profiles, Privacy choices
[more](https://www.tutorialspoint.com/machine_learning/index.htm#)
Cookie duration resets each session. Uses other forms of storage.
[View details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Storage details](https://www.tutorialspoint.com/machine_learning/index.htm#) | [Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
Ad partners
## Meta
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Roku Advertising Services
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## engageBDR
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Evidon
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## GroovinAds
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## HQ GmbH
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## intelliAd
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## iProspect
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Kwanzoo
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## MediaMath
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Sizmek
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## ZMS
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Mixpo
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## PlatformOne
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Smart
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## SMN Corporation
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Tapad
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Tradedoubler AB
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## TrustArc
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## TruEffect
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## 顶新
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## MicroAd
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Webgains
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## RevenueMantra
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## AdMaxim
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## LivelyImpact
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## LiquidM
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## KPI Solutions
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## MaxCDN
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Magnite
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## MoPub (a division of Twitter, Inc.)
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Yango
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Singular Labs Inc.
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Neustar
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Netquest
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Cloudflare
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Salesforce DMP
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Orange Advertising
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## GoldSpot Media
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## AppLovin Corp.
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## AdTheorent, Inc.
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## LINK Institut
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Rackspace
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Signal
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Chocolate Platform
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Navegg
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Kochava
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## OneDigitalAd Technologies
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Unitymedia
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Perfect Audience
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## GroundTruth
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Rontar
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Placed
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Impact
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Gruvi
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Spotad
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Aarki
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## F@N communications
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## SFR
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Tealium
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Vpon
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## NinthDecimal
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## TenMax
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## TreSensa
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## LotLinx®
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Tapjoy
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Kadam
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Optimize LCC D.B.A Genius Monkey
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## gskinner
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Yahoo! Japan
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Chalk Digital
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## OpenJS Foundation
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## KeyCDN
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## jsdelivr
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Upwave
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## JustWatch
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Expedia, Inc.
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## fluct
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Zucks
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Viant
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Dentsu Aegis Network
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Bidease
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## UNICORN
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Smart.bid ltd
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Maelico LTD
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## GroundhogTech
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## AdFalcon
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## KAYAK
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## NativeAds.com
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Supership
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Marketing Science Consulting Group, Inc.
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Reactive
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## DENTSU
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Kobler
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Parrable
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Native Touch
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Net Info
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## OpinionAds
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Widespace
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## AdPlay
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Tapklik
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## 北京泛为信息科技有限公司
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## ListenLoop
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Vimeo
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## X-Social
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Tail
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Oracle Data Cloud
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Yabbi
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Lucidity
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Throtle
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## ironSource Mobile
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## 世纪富轩科技发展（北京）有限公司
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## MediaPal
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Tuky Data
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Glassdoor, Inc.
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## CONTXTFUL
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Human Made Machine Limited
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## FLYWHEEL
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Inskin Media
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## MarketCast LLC
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Stream
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Go Mobile
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## 1plusX
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## The Very Group
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Kwanza DSP
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## OTM Worldwide LLC
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Wagawin
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Target RTB
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## MI DSP
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## OneDash
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Zynga
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Reset Digital Europe Ltd
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Kaden
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## tD-GDN
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## LINE
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Melvad
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## HueAds
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Unity Ads
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Loblaw Media
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## hyScore.io GmbH
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## HYP Pty Ltd
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## IAB Tech Lab
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Lacuna
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Xiaomi DSP
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Nimbus
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## MetaAds
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Indeed
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Playable Factory
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Glui
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Prism Partner
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Reliz Ad Platform
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## TemuDSP
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## mFilterIt
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
## Mercado Livre
[Privacy policy](https://www.tutorialspoint.com/machine_learning/index.htm#)
Consent
Accept all
Confirm choices
Close
