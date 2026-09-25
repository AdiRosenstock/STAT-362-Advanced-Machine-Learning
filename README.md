# STAT 362: Advanced Machine Learning for Data Science

Hi! This is my repo for **STAT 362: Advanced Machine Learning** at Northwestern University. I'm using it to keep my notes, class notebooks and exercise sets in one place while I take the course, and to show what I'm learning along the way. Everything is written in Python.

## About the class

STAT 362 builds on the Data Science sequence (STAT 301/303) and adds the math behind the models. We don't just call `.fit()`: we derive how Machine Learning and Deep Learning models work and then implement them, often from scratch first and then with libraries like scikit-learn and Keras.

The course starts with the different types of supervised learning tasks. It then moves on to unsupervised learning, recommendation engines and anomaly detection. The second half is about big data and why it calls for Deep Neural Networks, and it ends with specialized architectures for image and time-series data.

## What I'm aiming to get out of it

By the end of the quarter, I want to be able to:

- Set up a Machine Learning task in the right way for the problem.
- Derive and implement supervised learning models using Gradient Descent and Support Vector Machines.
- Build hard and soft clustering algorithms, both from scratch and with high-level libraries.
- Reduce the dimensionality of data, and know when that's actually necessary.
- Write short, practical ML software with scikit-learn and Keras.
- Detect anomalies like product malfunctions and credit card fraud.
- Understand Deep Learning theory well enough to build neural networks from scratch as well as with libraries.
- Design neural networks with specialized architectures for image and time-series data.

## Topics covered

| Week   | Topic                               |
| ------ | ----------------------------------- |
| 1      | Introduction and Recap              |
| 1 – 2  | Gradient Descent                    |
| 2 – 3  | Support Vector Machines             |
| 3      | More on Supervised Learning         |
| 4 – 5  | Clustering                          |
| 5 – 6  | Dimensionality Reduction            |
| 6 – 7  | Deep Neural Networks                |
| 8      | Convolutional Neural Networks       |
| 9      | Recurrent Neural Networks           |
| 10     | Transformers and Attention Networks |

## What's in here so far

- **`Notebook.ipynb`**: my running class notebook. It currently covers the intro to ML and linear regression with Gradient Descent, including plots of the cost surface, how the learning rate affects convergence, and the descent path down the "bowl."
- **`Exercises/Exercise_Set1/`**: my first exercise set. It explores the Banknote Authentication dataset (binary classification): checking the classes, features, missing values and zero values, plus some extra visualizations I made for myself.

I'll keep adding notebooks and exercise sets as the quarter goes on.

## Running the notebooks

If you'd like to run anything yourself:

```bash
git clone git@github.com:AdiRosenstock/STAT-362-Advanced-Machine-Learning.git
cd STAT-362-Advanced-Machine-Learning
pip install numpy pandas matplotlib scikit-learn tensorflow jupyter
jupyter notebook
```
