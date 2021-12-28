# URL Detective

A webapp based solution which identifies malicious URLs
using Machine Learning. 

## To Run

Clone the repository
```
git clone https://github.com/ASHWINK07/urldetective.git
cd urldetective
```
Build the model
```
cd data
python3 rfcmodel.py
```
Move the model to the main folder

```
mv RFCmodelfin.pkl ../
```
Run the webapp

```
cd ..

python3 app.py
```
## Run using Docker
Pull
```
docker pull ashwink07/urldetective:urldetective
```
Run
```
docker run -p 5000:5000 ashwink07/urldetective:urldetective
```
## How to use
Open the link displayed in your terminal and

Simply paste any link that you are suspicious about
and press GO!!!

![sample](https://user-images.githubusercontent.com/60002889/132223068-c5097477-de02-4b22-a3c4-4cbb8b5dfd4c.png)