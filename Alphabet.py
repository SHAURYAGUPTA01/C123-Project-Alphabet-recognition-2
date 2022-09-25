import cv2
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.datasets import fetch_openml

X = np.load('image.npz')['arr_0']
y = pd.read_csv("labels.csv")['labels']
print(pd.Series(y).value_counts())
classes = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
nclasses = len(classes)

x_train,x_test,y_train,y_test = train_test_split(X,y,random_state = 9,train_size = 7500,test_size = 2500)
x_trainscale = x_train/255.0
x_testscale = x_test/255.0
clf = LogisticRegression(solver = "saga", multi_class = "multinomial").fit(x_trainscale,y_train)
y_pred = clf.predict(x_testscale)
acc = accuracy_score(y_test,y_pred)
print(acc)

cap = cv2.VideoCapture(0)
while (True) :
    try : 
        ret,frame = cap.read()
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        height,width = gray.shape
        
        upper_left = (int(width/2-56),int(height/2-56) )
        bottom_right = (int(width/2+56),int(height/2+56) )
        cv2.rectangle(gray,upper_left,bottom_right,(0,255,0),2)
        roi = gray[upper_left[1]:bottom_right[1] ,upper_left[0]:bottom_right[0]]
        impil = Image.fromarray(roi)
        
        img_bw = impil.convert("L")
        img_bw_resize = img_bw.resize((28,28),Image.ANTIALIAS)
        img_inverted = PIL.ImageOps.invert(img_bw_resize)
        pixel_filter = 20
        min_pixel = np.percentile(img_inverted,pixel_filter)
        img_invertedscale = np.clip(img_inverted-min_pixel,0,255)
        max_pixel = np.max(img_inverted)
        img_invertedscale = np.asarray(img_invertedscale)/max_pixel
        
        test_sample = np.array(img_invertedscale).reshape(1,784)
        test_pred = clf.predict(test_sample)
        print("predicted digit classes : ", test_pred)
        
        cv2.imshow("Alphabet",gray)
        if cv2.waitKey(7000) & 0xFF == ord('q'):
            break
        
    except Exception as e:
        pass
    
cap.release()
cv2.destroyAllWindows()