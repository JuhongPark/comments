## Problem Set

# **LLM-Based YouTube Comment Analysis and Moderation**

Analyze and moderate YouTube comments using LLM classification and prompt engineering.

# **Overview**

This homework assignment centers on automating the analysis and moderation of YouTube video comments using a Large Language Model (LLM). You will extract comments, store them in a SQLite (note not MySQL) database, create prompts for comment moderation, perform analytics, and visualize the results. The assignment evaluates comment sentiments, relevance, and categorizes them while also focusing on creating responses and reporting analytics. Questions include sentiment analysis, response generation, categorization, and analytics reporting.
**SQLite tutorial**: [https://youtu.be/girsuXz0yA8](https://youtu.be/girsuXz0yA8)

# **Objective**

To gain practical experience with online data collection, database design, text classification using LLMs, and visualization techniques. You will analyze comments from a specific YouTube video, employing various data science and AI methodologies to moderate and categorize these comments effectively.

# **Video for Analysis \- Altman Interview (Duration: 2:23:56)**

You are going to be analyzing the YouTube video titled "Sam Altman: OpenAI CEO on GPT-4, ChatGPT, and the Future of AI''. Sam Altman discusses the intricacies of AI development, including challenges, strategic decisions, and future directions. This video offers a deep dive into the evolution of AI technologies and the ethical considerations surrounding them.

The URL is: [https://www.youtube.com/watch?v=L\_Guz73e6fw](https://www.youtube.com/watch?v=L_Guz73e6fw)

# **1 \- Extract "comments" from video, save to a json file**

**Note:** You will need to pull the data again \- the one from class is old.

**Objective**: Fetch comments from the specified YouTube video and save them as \`comments.json\`.

**Tools**: Use GitHub to find a YouTube comments downloader. Keywords like "YouTube comments downloader" or "YouTube API comments fetch" will be helpful.

**Code submission**: Once you have successfully downloaded the data, you will need to place your code in a file named "01\_extract.py". This script should automate the process of accessing the video, navigating to the relevant sections, and downloading the comments in JSON format.

Save the json you extracted to a file named, "comments.json"

# **2 \- Count the lines of json**

**Objective**: Count the total number of comments in your "comments.json" file.
**Code Submission**: Place your code in a script named "02\_count.py". This script should go through your data, identify the comments, and count the entries.

# **3 \- Create a "comments" database (SQLite)**

**Objective**: Create a 'comments' database using SQLite. Populate this database with data from your JSON file, ensuring each comment from the JSON data is represented as a new row in the database. For every attribute within the 'comment' JSON object, create a corresponding column in your database table. Add four additional fields to be used later: negative, angry, spam, and response.

| { "cid":         "placeholder", "text":        "placeholder", "time":        "placeholder", "author":      "placeholder", "channel":     "placeholder", "votes":       "placeholder", "photo":       "placeholder", "heart":       "placeholder", "reply":       "placeholder", "time\_parsed": "placeholder"  "negative":    "placeholder",  "angry":       "placeholder",  "spam":        "placeholder",  "response":    "placeholder"} |
| :---- |

**Code Submission**: Place your code in a script named "03\_database.py". When you run the script, the code should generate an SQLite database named, "comments.db".

# 4 \- Prompt Classification on a Sample Dataset

**Objective**: Compile a small sample of 25 comments, ensure it includes a mix of emotions and types: a few angry comments, some spam, negative comments, and at least one that necessitates a reply. Then, using the ChatGPT interactive console on the browser, construct a prompt that accurately classifies these comments into categories. Your goal is to receive a JSON response like the one below:

| {"angry": true, "negative": true, "response": true, "spam": false} |
| :---- |

**Code Submission**: Save your sample data in a file named, "sample\_data.json". Save your prompt in a file named, "prompt.txt".

# 5 \- Ping LLM

**Objective**: Your task is to demonstrate proficiency in using an open source LLM, using Ollama, by sending a specific question and receiving a response in a predefined JSON format. Pose the following question to the LLM: "How many states are there in the United States of America?" Ensure the response is formatted as a JSON object with a key-value pair as shown below. Example format for clarity:

| {  "answer": "Your response here"} |
| :---- |

**Code Submission**: Place your code in a script named "05\_ping\_llm.py".

# 6 \- Predict four factors

Pick the first 100 comments to work with. When you are done with all questions in the problem set, do a run with all the comments.

Select an LLM from the list of LLMs in Ollama. You can select any LLM you like but it must fit in a CodeSpace:

| https://ollama.com/search |
| :---- |

Create a prompt within a python program and call the LLM to classify the comments. Evaluate the comments for sentiment, anger, spam, and the necessity for a response. Update the database with your findings.

For each comment:

* Determine the sentiment: Is it positive or negative?
* Identify anger: Is the comment angry?
* Detect spam: Is the comment spam?
* Assess relevance and response necessity: Does the comment pertain to the topic? Does it require a response?

**Code Submission**: Place your code in a script named "06\_prediction.py".

# 7 \- Create responses

Add a new column in the "comments" table called "responses". Then, write responses to the comments you identified in question 06\. Add your responses to the new database column.

**Code Submission**: Place your code in a script named "07\_create\_responses.py".

# 8 \- Comment categories

Are there categories in the comments made by viewers? For example, is there a number of comments that raise ethical concerns. If yes, what are the categories?

**Code Submission**: Place your code in a script named "08\_categories.py".

# 9 \- Embeddings and Clustering Visualization

**Objective**: Use embeddings to represent the comments in a high-dimensional space and apply K-means clustering to identify patterns in the comments. Then, use t-SNE or another dimensionality reduction technique to visualize the clusters.

**Steps**:

1. **Convert comments into embeddings**:
   * Use a pre-trained sentence embedding model to convert each comment into a vector representation.
2. **Apply K-means clustering**:
   * Choose an appropriate number of clusters (e.g., 4–6).
   * Cluster the embedded comments using K-means.
3. **Reduce dimensions for visualization**:
   * Use t-SNE or PCA to project the embeddings into 2D space for visualization.
4. **Visualize the clusters**:
   * Create a scatter plot where each point represents a comment, colored by its assigned cluster.
   * Mark the centroid of each cluster.
5. **Analyze the clusters**:
   * Examine the comments in each cluster. Are there common themes? Do they align with existing categories such as positive, negative, angry, or spam?

**Code Submission**:

* Place your code in a script named "09\_visualization.py".
* Your visualization should be generated using Python libraries such as Matplotlib, Seaborn, or Plotly.

# 10 \- Create a python requirements file

Create a "requirements.txt" file that includes all the python packages you used in the problem set. This file should list all the external libraries your project depends on. After creating the file, write a Python script named "setup\_requirements.py" that uses the \`subprocess\` module to install all dependencies listed in your "requirements.txt" file automatically.

For example:

| import subprocessimport sys\# install dependencies from a requirements.txt filedef install\_requirements(requirements\_path):   subprocess.check\_call(\[sys.executable, "-m", "pip", "install", "-r", requirements\_path\])\# Example usagerequirements\_path \= './requirements.txt'install\_requirements(requirements\_path) |
| :---- |

This script defines a function "install\_requirements" that takes the path to your "requirements.txt" file as an argument. It then uses "subprocess.check\_call" with "sys.executable" to ensure that the pip command is executed with the same Python interpreter that runs the script, which is particularly useful if you have multiple Python environments.

### Explanation:

The \`requirements.txt\` file is crucial for managing project dependencies in a consistent environment, ensuring that anyone who runs your project has the right versions of the necessary libraries. The "setup\_requirements.py" script you write will streamline the setup process for your project, making it easy to get up and running with just a couple of commands. This approach is especially useful for projects shared across teams or deployed in different environments, promoting consistency and reducing setup errors.

# 11 \- Export a Clean Formatted Dataset of your Entire database:

Objective: The final step in your data journey involves preparing and exporting a clean, well-formatted dataset of your database. Name the file "clean\_dataset.json". Instead of going from JSON to database, you will now be going from database to JSON.

Code Submission: Your clean and formatted dataset should be produced by a script named "11\_export.py". This script should automate the process of exporting the data. Document your file's structure, including descriptions of columns, data types, and any assumptions or decisions made during the data preparation process.

# 12 \- Data pipeline

Write a program that automates the sequential execution of all the previously created script files, ensuring that each script runs to completion before the next begins. This program aims to streamline the generation of outputs from all your previous  files, consolidating the results into one sequence. This script should be designed to programmatically call and execute each of the prior scripts in the correct order:

* Install requirements (setup\_requirements.py, requirements.txt)
* Extract data (01\_extract.py, comments.json)
* Count comments (02\_count.py)
* Create database (03\_database.py, comments.db)
* Sample data (sample\_data.json, prompt.txt)
* OpenAI API (05\_ping\_openai.py)
* Comment analysis (06\_prediction.py)
* Create responses (07\_create\_responses.py)
* Extract categories (08\_categories.py)
* Create visualization (09\_visualization.py)
* Final dataset, (clean\_dataset.json)

Your script should handle any dependencies between scripts, ensuring that output from one step is correctly inputted into the next. It should also include error handling to manage any issues that arise during execution, ensuring the entire pipeline can run smoothly from start to finish without manual intervention.

Code Submission:: Place your code in "12\_pipeline.py"
